import 'package:flutter/material.dart';

class TrimestralScreen extends StatelessWidget {
  const TrimestralScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Encuesta Trimestral")),
      body: const Center(
        child: Text("Aquí va la encuesta trimestral"),
      ),
    );
  }
}
