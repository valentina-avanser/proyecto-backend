import 'package:flutter/material.dart';
import 'inscripcion.dart'; // Importamos la nueva pantalla de inscripción

class ConvocatoriasScreen extends StatelessWidget {
  const ConvocatoriasScreen({super.key});

  final List<Map<String, String>> convocatorias = const [
    {
      "titulo": "Primer tipo de sostenimiento",
      "tipo": "Apoyo de sostenimiento",
      "detalles": "Apoyo económico para aprendices en condición de vulnerabilidad.",
      "fechaInicio": "01/10/2025",
      "fechaLimite": "15/10/2025",
      "duracion": "6 meses",
      "cupos": "17/134"
    },
    {
      "titulo": "Convocatoria Monitorías 2025",
      "tipo": "Monitorías",
      "detalles": "Apoyo a instructores mediante monitorías académicas.",
      "fechaInicio": "05/10/2025",
      "fechaLimite": "20/10/2025",
      "duracion": "4 meses",
      "cupos": "9/50"
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Convocatorias"),
        backgroundColor: Colors.green[700],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: convocatorias.length,
        itemBuilder: (context, index) {
          final conv = convocatorias[index];

          return GestureDetector(
            onTap: () {
              // 🚀 Redirige a la pantalla de inscripción y pasa la info de la convocatoria
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => InscripcionScreen(convocatoria: conv),
                ),
              );
            },
            child: Card(
              elevation: 4,
              margin: const EdgeInsets.symmetric(vertical: 12),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Título + Tipo + Icono PDF
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                conv["titulo"]!,
                                style: const TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.black87,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                conv["tipo"]!,
                                style: const TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w500,
                                  color: Colors.green,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const Icon(Icons.picture_as_pdf,
                            color: Colors.red, size: 30),
                      ],
                    ),

                    const SizedBox(height: 10),

                    // Detalles
                    Text(
                      conv["detalles"]!,
                      style:
                          const TextStyle(fontSize: 14, color: Colors.black87),
                    ),

                    const Divider(height: 20),

                    // Fechas y cupos
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text("Inicio: ${conv["fechaInicio"]}"),
                            Text("Cierre: ${conv["fechaLimite"]}"),
                            Text("Duración: ${conv["duracion"]}"),
                          ],
                        ),
                        Text(
                          "Cupos: ${conv["cupos"]}",
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                            color: Colors.blueGrey,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
