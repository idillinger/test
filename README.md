# Scheduled Ride Sharing App

This repository contains a minimal proof of concept for an employee ride sharing service. The focus is on using **free or open‑source** services that operate in **Jordan**.

## Technology Choices

- **Backend:** Node.js with built-in modules. No paid dependencies required.
- **Maps & Routing:** [OpenStreetMap](https://www.openstreetmap.org/) data with routing via [OpenRouteService](https://openrouteservice.org/) or [OSRM](http://project-osrm.org/). These services provide free tiers and cover Jordan.
- **SMS Verification:** [Firebase Phone Authentication](https://firebase.google.com/docs/auth) offers a generous free tier and supports Jordanian numbers.
- **Payments:** [HyperPay](https://www.hyperpay.com/) operates in Jordan and supports card payments. Integration is free; transaction fees apply.

## Development

```
cd server
npm test    # runs basic tests using Node's built-in test runner
```

### GitHub Pages Hosting

A GitHub Actions workflow builds the Flutter web prototype and publishes it to GitHub Pages whenever changes land on `main`. After pushing, the app will be available at:

```
https://<your-user>.github.io/<this-repo>/
```

The Node.js server remains a placeholder for future API work but is not required to view the hosted web prototype.

## Future Work

- Mobile applications (Flutter or React Native) targeting Android and iOS.
- Secure authentication flow, database persistence, and cost-sharing algorithm.
- Integration with mapping, SMS, and payment providers mentioned above.

