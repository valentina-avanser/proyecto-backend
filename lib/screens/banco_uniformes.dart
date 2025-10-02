import 'package:flutter/material.dart';

class BancoUniformesScreen extends StatelessWidget {
  const BancoUniformesScreen({super.key});

  final List<Map<String, dynamic>> uniformes = const [
    {
      "tipo": "Overol de mecánica",
      "estado": "Buen estado",
      "detalle": "Sin manchas, costuras firmes.",
      "distintivo": "Sí (Mecánica Automotriz)",
      "disponible": true,
      "imagen":
          "https://cdn-icons-png.flaticon.com/512/679/679922.png", // ejemplo
    },
    {
      "tipo": "Bata de laboratorio",
      "estado": "Estado medio",
      "detalle": "Tiene ligeras manchas en mangas.",
      "distintivo": "No",
      "disponible": false,
      "imagen":
          "https://cdn-icons-png.flaticon.com/512/1055/1055644.png", // ejemplo
    },
    {
      "tipo": "Camiseta de formación",
      "estado": "Nuevo",
      "detalle": "Nunca usada, entrega reciente.",
      "distintivo": "Sí (Sistemas)",
      "disponible": true,
      "imagen":
          "https://cdn-icons-png.flaticon.com/512/892/892458.png", // ejemplo
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Banco de Uniformes"),
        backgroundColor: Colors.green[700],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: uniformes.length,
        itemBuilder: (context, index) {
          final uni = uniformes[index];

          return Card(
            elevation: 4,
            margin: const EdgeInsets.symmetric(vertical: 12),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Imagen
                  ClipRRect(
                    borderRadius: BorderRadius.circular(12),
                    child: Image.network(
                      uni["imagen"],
                      height: 80,
                      width: 80,
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) {
                        return Container(
                          height: 80,
                          width: 80,
                          color: Colors.grey[300],
                          child: const Icon(Icons.checkroom,
                              size: 40, color: Colors.grey),
                        );
                      },
                    ),
                  ),
                  const SizedBox(width: 16),

                  // Información del uniforme
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Tipo
                        Text(
                          uni["tipo"],
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),

                        const SizedBox(height: 6),

                        // Estado
                        Text(
                          "Estado: ${uni["estado"]}",
                          style: TextStyle(
                            fontSize: 14,
                            color: uni["estado"] == "Nuevo"
                                ? Colors.green
                                : (uni["estado"] == "Buen estado"
                                    ? Colors.blue
                                    : Colors.orange),
                          ),
                        ),

                        // Detalle debajo del estado
                        Text(
                          uni["detalle"],
                          style: const TextStyle(
                            fontSize: 12,
                            color: Colors.black54,
                          ),
                        ),

                        const SizedBox(height: 6),

                        // Distintivo
                        Text("Distintivo: ${uni["distintivo"]}",
                            style: const TextStyle(fontSize: 14)),

                        const SizedBox(height: 6),

                        // Disponibilidad
                        Row(
                          children: [
                            Icon(
                              uni["disponible"]
                                  ? Icons.check_circle
                                  : Icons.cancel,
                              color: uni["disponible"]
                                  ? Colors.green
                                  : Colors.red,
                              size: 18,
                            ),
                            const SizedBox(width: 6),
                            Text(
                              uni["disponible"]
                                  ? "Disponible"
                                  : "No disponible",
                              style: TextStyle(
                                color: uni["disponible"]
                                    ? Colors.green
                                    : Colors.red,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ],
                        )
                      ],
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
