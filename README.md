# CommutePool — A Scheduled, Shared Commute App (Like Uber, but for employees)

A concise, end-to-end build plan in markdown. Use this as the blueprint for product, design, engineering, security, and ops.

---

## 1) Product Vision

* **What:** Scheduled, shared rides for employees going to nearby destinations at similar times.
* **Why:** Cut daily commute cost by grouping riders, auto-routing pickups/drop-offs, and **fairly splitting** the fare by who rides how far/long.
* **How:** Pre-booked trips (morning/evening), card-only payment with pre-auth at boarding and capture at trip end, driver payout after completion.

---

## 2) Core User Roles

* **Rider (employee):** Registers, verifies phone, sets work schedule & pickup point, joins/creates a scheduled commute, pays card-only.
* **Driver:** KYC-verified, defines capacity/time windows, accepts scheduled trips, navigates provided route, gets paid post-trip.
* **Ops/Admin:** Reviews KYC, handles disputes/chargebacks, manages service areas, promotions, pricing rules, risk flags.
* **Employer (optional):** Can sponsor routes, import staff list, set pickup hubs, subsidize fares.

---

## 3) Mobile App UX (Flutter recommended, iOS/Android)

### 3.1 Onboarding & Auth

* **Screens:**

  1. Welcome → Sign in / Register
  2. Enter Phone Number → **SMS OTP** verification
  3. Profile: Full name, email (optional work email), company (optional), preferred language
  4. Add **Workplace** (address/place ID), working days, **arrival time window** (e.g., arrive by 8:30–8:45)

* **Requirements:**

  * SMS/OTP provider (e.g., Twilio Verify/MessageBird).
  * Device binding & re-verification on suspicious devices.

### 3.2 Home (Rider)

* **Header:** Company/workplace; change week/day.
* **Cards:**

  * “**Nearby scheduled trips**” (tile list: latest pickup within radius, ETA to work)
  * “**Create a new scheduled trip**” (pick day(s), pickup point, arrival window, seat count needed)
* **CTA Bar:**

  * “Join Trip”, “Create Trip”, “My Schedule” (calendar view).

### 3.3 Trip Creation / Join Flow (Rider)

* Set **pickup** (map pin or saved home), **days** (M–F), **arrival window**, **max walk** (e.g., 300 m), **price estimate** preview.
* Show **candidate groups** (2–6 riders) sorted by fit: proximity/time, price, detour.
* Payment setup (card tokenization). **Pre-auth policy** shown.

### 3.4 Live Trip (Rider)

* Pre-boarding: “Driver on the way” with ETA and **boarding QR**.
* In-Trip: live map, next stop, remaining time, running **fair-fare** meter (est. range).
* Post-Trip: final receipt breakdown, tip (optional), rating.

### 3.5 Driver App

* **Today’s Schedule** with trips (AM/PM), capacity left.
* Pre-trip checklist, navigation (deep link to Maps), **stop list** with boarding QR scan.
* Post-trip summary, payout estimate.

### 3.6 Settings

* Cards (add/remove; default), receipts, notifications, help, privacy, logout.

---

## 4) Fair Fare — Pricing & Cost Split

**Goals:** budget-balanced, monotonic (longer riders pay more), transparent.

### 4.1 Cost Model

* **Trip cost** = BasePlatformFee + DriverTimeCost + DistanceCost + Tolls/Fees − Discounts.
* Estimate **DistanceCost** and **TimeCost** using the planned route from the Directions API (traffic-aware ETA, arrive-by).

### 4.2 Segment-Share Algorithm (simple, fair, real-time)

1. Build ordered route segments between each consecutive stop `s`.
2. For each segment `s`, compute **cost\_s** = `α·distance_s + β·time_s + tolls_s`.
3. Let **N\_s** be number of riders aboard during segment `s`.
4. Each rider aboard pays `cost_s / N_s`.
5. Add rider **BaseRiderFee** (small booking fee) + taxes.
6. Apply caps/floors and round to sensible currency units.

**Why:** The rider who drops earlier rides fewer segments → pays less. No rider subsidizes others beyond shared time on board.

> Optionally, add a **Shapley approximation** as an advanced mode to validate fairness on batch runs.

---

## 5) Matching & Routing

### 5.1 Problem

* **Inputs:** Rider pickup points, arrival time windows, capacity, driver start location.
* **Objective:** Minimize total cost/time subject to constraints (arrive-by windows, max detour, seat capacity).

### 5.2 Practical Solution (MVP → Advanced)

* **MVP Heuristic:**

  * Cluster riders by destination & arrival window (DBSCAN/HDBSCAN on (lat, lon, arrival\_time)).
  * Within a cluster, build a pickup order via nearest-insertion heuristic that respects **latest arrival**.
  * Evaluate multiple candidate permutations; pick min cost.

* **Phase 2 (Optimization):**

  * Use **Google OR-Tools** for **CVRPTW** (vehicle routing with time windows) with pickup nodes; constraints: capacity, max ride time, max detour, latest arrival.
  * Edge weights from **Distance Matrix API** (arrive-by). Cache for performance.

### 5.3 Schedule Cadence

* Recompute routes nightly for next day; re-optimize hourly for late changes; lock route T-15min.

---

## 6) Payments (Card-Only, 3DS2, Pre-Auth + Capture)

* **Gateway:** PSP with tokenization, 3DS2, network token support, split payouts (e.g., Stripe/Adyen/Checkout.com/Paymob/HyperPay).

* **Flow:**

  1. Rider adds card → **tokenized**; store only token, never PAN.
  2. **At boarding (QR scan):** Pre-authorize **max\_estimate + buffer** (e.g., 20%).
  3. **At trip end:** Capture **actual fare**, release excess hold.
  4. **Payouts:** Driver receives net (fare − platform fee − taxes) via PSP **Connect/Marketplace** flow after trip completion (daily batch).
  5. **Failures:** If capture fails, retry, use backup card, apply soft-ban until settled.

* **Security/Compliance:** PCI-DSS scope minimized (SAQ A), SCA/3DS2, dispute webhooks, chargeback handling.

---

## 7) System Architecture

### 7.1 High-Level (Mermaid)

```mermaid
flowchart LR
  A[Flutter Apps (iOS/Android)] -- HTTPS --> B(API Gateway)
  B --> C[NestJS/FastAPI Backend]
  C --> D[(Postgres + PostGIS)]
  C --> E[(Redis: cache/queues)]
  C --> F[Route Solver svc (Python + OR-Tools)]
  C --> G[PSP (Cards, 3DS2)]
  C --> H[SMS/OTP Provider]
  C --> I[Maps: Geocode, Directions, Matrix]
  C --> J[Object Storage (receipts, logs)]
  C --> K[Analytics/BI]
  C --> L[Notifications (FCM/APNs)]
  C --> M[Observability (Logs/Trace/Metrics)]
```

### 7.2 Tech Stack

* **Mobile:** Flutter, Riverpod/Bloc, Dio, Google Maps SDK, Firebase Messaging.
* **Backend:** Node.js (NestJS) or Python (FastAPI); REST + Webhooks; Swagger/OpenAPI.
* **DB:** Postgres + PostGIS (geospatial), Redis (rate-limit, sessions, jobs).
* **Routing:** Python microservice with OR-Tools; Celery/RQ workers.
* **Infra:** Docker, Docker Compose (MVP) → Kubernetes (prod). Nginx Ingress, Let’s Encrypt TLS.
* **CI/CD:** GitHub Actions; unit/integration/E2E pipelines; fastlane for mobile builds.

---

## 8) Data Model (Key Entities)

* **User**(id, phone\_e164, name, email, role, status, created\_at)
* **RiderProfile**(user\_id FK, company\_id FK, default\_pickup\_geom, max\_walk\_m, prefs)
* **DriverProfile**(user\_id FK, license\_no, vehicle\_id, capacity, KYC\_status)
* **Vehicle**(id, make, model, plate, capacity, insurance\_expiry, color)
* **PaymentMethod**(user\_id, psp\_customer\_id, token\_id, brand, last4, exp\_month/year, default)
* **TripTemplate**(id, destination\_geom, arrival\_window\_start/end, weekdays\_bitmask)
* **TripInstance**(id, date, state, driver\_id, vehicle\_id, route\_polyline, start\_time, end\_time)
* **Stop**(id, trip\_instance\_id, type\[pickup/drop], order, geom, eta, etd)
* **TripRider**(trip\_instance\_id, rider\_id, status, boarded\_at, dropped\_at, seat\_position)
* **FareSegment**(trip\_instance\_id, seg\_index, distance\_m, time\_s, riders\_onboard\_json)
* **FareCharge**(trip\_instance\_id, rider\_id, base\_fee, variable\_fee, tax, total, currency, psp\_auth\_id, psp\_capture\_id, status)
* **Payout**(driver\_id, amount, currency, psp\_transfer\_id, status, scheduled\_for)
* **KYC/Docs**(user\_id, doc\_type, uri, status)
* **AuditLog**(who, action, when, payload\_hash)

> Use **PostGIS** for geometry (pickup, destination, route).

---

## 9) Public API (Representative Endpoints)

* `POST /auth/otp/send` → {phone}
* `POST /auth/otp/verify` → {phone, code} → JWT
* `GET /me` / `PATCH /me`
* `POST /payment-methods` (token from PSP)
* `GET /trips/nearby?lat=&lng=&time=`
* `POST /trips` (create scheduled commute request)
* `POST /trips/{id}/join` / `POST /trips/{id}/leave`
* `GET /trips/{id}` (itinerary, price estimate, fair-fare explainer)
* `POST /trips/{id}/board` (driver scans rider QR → pre-auth)
* `POST /trips/{id}/complete` (driver)
* `GET /receipts/{id}`
* Webhooks: `/webhooks/psp`, `/webhooks/sms`.

---

## 10) Matching & Fare Pseudocode

### 10.1 Matching (Heuristic MVP)

```pseudo
clusters = HDBSCAN(points=[(lat, lon, arrival_time)], min_cluster_size=3)
for cluster in clusters:
  candidates = permutations_or_nearest_insertion(cluster.riders)
  best = argmin_cost_feasible(candidates, constraints: arrive_by, capacity, max_detour)
  assign(best to a driver with compatible schedule)
```

### 10.2 Segment-Share Fare

```pseudo
total = 0
for segment in route.segments:
  cost_s = alpha * segment.distance_m + beta * segment.time_s + segment.tolls
  riders_onboard = segment.riders
  for r in riders_onboard:
    r.share += cost_s / len(riders_onboard)
  total += cost_s

for r in riders:
  r.total = round_currency(BaseRiderFee + r.share + taxes(r))
```

---

## 11) Security & Privacy (Install “all the security systems”)

* **Auth:** SMS OTP + device binding; JWT with short TTL + refresh; revoke on device change.
* **PSP:** Tokenize cards; **no PAN** on our servers; enforce **3DS2**; risk scoring & SCA step-up.
* **Transport:** TLS 1.2+; HSTS; secure cookies (httpOnly, SameSite).
* **Data at Rest:** PII encrypted (AES-256) using KMS; field-level encryption for phone, email.
* **Access:** RBAC/ABAC for admin; secrets in Vault/SSM; key rotation; least privilege.
* **API Hardening:** Rate limits, WAF, IP throttling, request signing for webhooks, idempotency keys.
* **Mobile AppSec:** Secure storage (Keychain/Keystore), jailbreak/root checks, cert pinning, obfuscation (ProGuard), screenshot protections for sensitive screens.
* **Compliance:** PCI-DSS (SAQ A/A-EP), privacy policy, data retention & deletion, consent for location tracking, local data protection laws.
* **Monitoring:** Anomaly detection for ghost rides, collusion, card testing; fraud rules; audit logs tamper-evident.

---

## 12) Operations & Support

* **SLOs:** API p95 < 300 ms, routing job < 5 s (cached), OTP delivery p95 < 10 s.
* **Observability:** Centralized logs, traces, dashboards (latency, auth errors, payment failures, match rate).
* **Alerting:** On-call rotations; alerts for auth spikes, drop in pre-auth success, routing errors.
* **CS Tools:** Refunds, manual re-price, driver/rider bans, document re-KYC.

---

## 13) Deployment & Environments

### 13.1 Envs

* **Dev** (feature branches), **Staging** (test cards, sandbox OTP), **Prod**.

### 13.2 Minimal Server Setup (MVP)

1. Provision VM(s) or managed services (DB, Redis).
2. `docker-compose` services: api, solver, worker, nginx, redis.
3. Postgres (managed preferred) with automated backups; PostGIS enabled.
4. DNS + TLS via Let’s Encrypt; enable HSTS.
5. CI/CD: GitHub Actions → build containers → deploy to server via SSH or to K8s.

### 13.3 Kubernetes (Phase 2)

* Ingress (Nginx), Horizontal Pod Autoscaler, secrets in KMS/Secrets Manager, autoscaled workers, node pools for CPU-heavy solver.

---

## 14) Testing Strategy

* **Unit:** pricing, segment share math, time windows, OTP flows.
* **Integration:** PSP sandbox (auth/capture/refund), SMS provider, Maps API.
* **E2E:** happy paths for create/join/board/complete, failure paths (capture fail).
* **Security:** OWASP ASVS checks, dependency SCA, DAST on staging.
* **Load:** Distance Matrix caching, hot clusters at peak (7–9 AM, 5–7 PM).

---

## 15) Policies & Edge Cases

* **No-Show:** pre-auth cancel fee (small) if driver waited ≥X minutes.
* **Late Rider:** dynamic reorder if still feasible; otherwise mark absent.
* **Cancellations:** free till T-30min; partial after.
* **Driver Cancel:** platform credits + re-assignment; reliability scoring.
* **Capacity Overflows:** enforce at join; seat belt reminder.
* **Safety:** SOS, share live trip, driver identity verification, vehicle photo.

---

## 16) Employer Features (Optional, High Impact)

* **Employer Hubs:** fixed drop zones at campuses.
* **Roster Import:** CSV or SSO domain claim; bulk invite.
* **Subsidies:** % or fixed amount per rider/day; monthly invoicing.
* **Analytics:** on-time rate, CO₂ saved, cost per employee.

---

## 17) Roadmap (Phased)

* **Phase 0 – Prototype (2–4 wks):** OTP auth, add card (sandbox), create/join trip, static route & segment split, mock payouts.
* **Phase 1 – MVP (4–8 wks):** Live routing with Matrix API, pre-auth at boarding, capture at end, receipts, driver KYC, basic ops console.
* **Phase 2 – Scale:** OR-Tools solver, dynamic re-routing, employer hubs, subsidies, fraud rules, Kubernetes, analytics.
* **Phase 3 – Polish:** Gamification, loyalty, guaranteed ride backup, pooled subscriptions.

---

## 18) Config & Tuning

* **α / β (distance vs time):** tune by market fuel/electricity & wage.
* **Buffer for pre-auth:** start 20%, learn from variance.
* **Max Detour:** 15–20% of direct ETA (per market).
* **Cluster Radius:** start 2–5 km around destination within 10–15 min arrival window.
* **Min/Max Group Size:** 3–6 riders per vehicle (plus driver).

---

## 19) Deliverables Checklist

* [ ] Flutter apps (Rider & Driver) with QA builds (TestFlight/Play Internal).
* [ ] Backend (OpenAPI doc), Postgres + PostGIS, Redis.
* [ ] Route Solver microservice (heuristic MVP + OR-Tools ready).
* [ ] PSP integration (tokenize, pre-auth, capture, payouts), 3DS2.
* [ ] SMS/OTP integration with fallback.
* [ ] Admin panel (KYC, trips, refunds, flags).
* [ ] Observability (logs/traces/metrics) + alerting.
* [ ] Security hardening checklist passed (see §11).
* [ ] Runbook & on-call rota.
* [ ] Legal: Terms, Privacy, consent screens, data retention.

---

## 20) Developer Notes / Packages (Flutter)

* **State:** Riverpod/Bloc
* **HTTP:** Dio with interceptors (retry, auth refresh)
* **Maps:** google\_maps\_flutter, geolocator, geocoding
* **Payments:** PSP SDK (native platform channel if required)
* **QR:** qr\_flutter & barcode\_scanner
* **Push:** firebase\_messaging
* **Crash:** Sentry/Crashlytics
* **Analytics:** Amplitude/Mixpanel (consent-aware)

---

## 21) Example: Rider Fare Breakdown (Segment-Share)

* Segments:

  * S1 (Home A → Pickup B): riders aboard = {A,B} → cost S1 split 50/50
  * S2 (Pickup B → Office Street): riders aboard = {A,B,C} → cost S2 split 1/3 each
  * S3 (Office Street → Final Office Gate): riders aboard = {A,C} → cost S3 split 50/50
* Rider **B** pays only S1 + S2 shares (drops earlier), **C** pays S2 + S3 (rides longer).

**Transparent receipt** lists per-segment shares, base fee, tax, total.

---

## 22) “100% Secure” Reality Check

* Absolute security doesn’t exist, but you can **minimize risk**:

  * Keep raw card data **out of scope** (tokenize via PSP).
  * Enforce 3DS2 + risk checks on suspicious transactions.
  * Encrypt PII, rotate keys, strict access controls.
  * Continuous monitoring, rapid patching, incident response plan.

---

## 23) Launch Plan

1. **Pilot** with one employer campus, limited area & hours.
2. Calibrate pricing α/β, buffers, cluster size, detour caps.
3. Collect feedback, harden ops, expand radius/employers.
4. Marketing: refer-a-coworker, employer subsidies, “Green Commute” badges.

---

**That’s the full build plan.**
If you want, I can turn this into:

* a clickable Flutter screen map (widget tree & routes),
* a Postgres schema SQL starter,
* OR-Tools solver skeleton,
* or a Docker Compose file to run the stack locally.
