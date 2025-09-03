import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final trips = const [
      {'route': 'Downtown → Business Park', 'time': '08:00'},
      {'route': 'West Amman → Tech Hub', 'time': '08:15'},
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Upcoming Trips')),
      body: ListView.builder(
        itemCount: trips.length,
        itemBuilder: (context, index) {
          final trip = trips[index];
          return ListTile(
            title: Text(trip['route']!),
            subtitle: Text('Departs at ${trip['time']}'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Join trip coming soon')),
              );
            },
          );
        },
      ),
    );
  }
}
