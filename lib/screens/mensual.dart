import 'package:flutter/material.dart';

class MensualScreen extends StatelessWidget {
  const MensualScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Encuesta Mensual")),
      body: const Center(
        child: Text("Aquí va la encuesta mensual"),
      ),
    );
  }
}
