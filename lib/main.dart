import 'package:flutter/material.dart';

void main() {
  runApp(const CommutePoolApp());
}

class CommutePoolApp extends StatelessWidget {
  const CommutePoolApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CommutePool',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Text('Welcome to CommutePool!'),
      ),
    );
  }
}
