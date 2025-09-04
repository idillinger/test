import 'package:flutter/material.dart';

/// An example page that displays a simple greeting.
class TestPage extends StatelessWidget {
  const TestPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Test Page')),
      body: const Center(child: Text('Hello from Test Page')),
    );
  }
}
