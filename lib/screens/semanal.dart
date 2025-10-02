import 'package:flutter/material.dart';

class SemanalScreen extends StatelessWidget {
  const SemanalScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Encuesta Semanal")),
      body: const Center(
        child: Text("Aquí va la encuesta semanal"),
      ),
    );
  }
}
