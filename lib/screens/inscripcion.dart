import 'package:flutter/material.dart';

class InscripcionScreen extends StatelessWidget {
  final Map<String, String> convocatoria;

  const InscripcionScreen({super.key, required this.convocatoria});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Inscripción - ${convocatoria["titulo"]}"),
        backgroundColor: Colors.green[700],
      ),
      body: Center(
        child: Text(
          "Formulario de inscripción para:\n${convocatoria["titulo"]}\n(${convocatoria["tipo"]})",
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}
