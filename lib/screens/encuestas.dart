import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

// Importamos las otras pantallas
import 'semanal.dart';
import 'mensual.dart';
import 'trimestral.dart';

class EncuestasScreen extends StatelessWidget {
  const EncuestasScreen({super.key});

  // Lista de encuestas con su pantalla asociada
  final List<Map<String, dynamic>> encuestas = const [
    {
      "titulo": "Encuesta Semanal",
      "detalle": "Comparte tu experiencia semanal con la formación.",
      "pantalla": SemanalScreen(),
    },
    {
      "titulo": "Encuesta Mensual",
      "detalle": "Ayúdanos a mejorar evaluando el proceso de este mes.",
      "pantalla": MensualScreen(),
    },
    {
      "titulo": "Encuesta Trimestral",
      "detalle": "Tu opinión es clave para el seguimiento del trimestre.",
      "pantalla": TrimestralScreen(),
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Encuestas"),
        backgroundColor: Colors.green[700],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: encuestas.length,
        itemBuilder: (context, index) {
          final encuesta = encuestas[index];

          return Card(
            elevation: 4,
            margin: const EdgeInsets.symmetric(vertical: 10),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15),
            ),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Título
                  Text(
                    encuesta["titulo"]!,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.green,
                    ),
                  ),
                  const SizedBox(height: 8),

                  // Detalle
                  Text(
                    encuesta["detalle"]!,
                    style: const TextStyle(fontSize: 14, color: Colors.black87),
                  ),
                  const SizedBox(height: 12),

                  // Botón abrir encuesta
                  Align(
                    alignment: Alignment.centerRight,
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green[700],
                        padding: const EdgeInsets.symmetric(
                            horizontal: 14, vertical: 10),
                      ),
                      icon: const Icon(FontAwesomeIcons.clipboardList,
                          color: Colors.white),
                      label: const Text(
                        "Responder Encuesta",
                        style: TextStyle(color: Colors.white),
                      ),
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => encuesta["pantalla"],
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
