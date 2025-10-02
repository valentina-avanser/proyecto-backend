import 'package:flutter/material.dart';

class NotificacionesScreen extends StatelessWidget {
  const NotificacionesScreen({super.key});

  // Lista de notificaciones de ejemplo
  final List<Map<String, String>> notificaciones = const [
    {
      "titulo": "Nueva Convocatoria",
      "detalle": "Se abrió la convocatoria para el programa de formación en Desarrollo de Software.",
      "hora": "10:45 AM"
    },
    {
      "titulo": "Recordatorio de Encuesta",
      "detalle": "Por favor, completa la encuesta de satisfacción antes del 05/10/2025.",
      "hora": "09:15 AM"
    },
    {
      "titulo": "Cambio de Horario",
      "detalle": "Tu clase de mañana ha sido reprogramada para las 2:00 PM.",
      "hora": "Ayer, 6:30 PM"
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Notificaciones"),
        backgroundColor: Colors.green[700],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: notificaciones.length,
        itemBuilder: (context, index) {
          final notif = notificaciones[index];

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
                    notif["titulo"]!,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.green,
                    ),
                  ),
                  const SizedBox(height: 8),

                  // Detalles
                  Text(
                    notif["detalle"]!,
                    style: const TextStyle(fontSize: 15, color: Colors.black87),
                  ),
                  const SizedBox(height: 10),

                  // Hora y botón
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        notif["hora"]!,
                        style: TextStyle(
                          fontSize: 13,
                          color: Colors.grey[600],
                        ),
                      ),
                      ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green[700],
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        ),
                        icon: const Icon(Icons.email, size: 18, color: Colors.white),
                        label: const Text(
                          "Enviar al correo",
                          style: TextStyle(color: Colors.white),
                        ),
                        onPressed: () {
                          // Aquí iría la lógica real de envío de correo
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(
                                "Notificación enviada a tu correo 📩: ${notif["titulo"]}",
                              ),
                              duration: const Duration(seconds: 2),
                            ),
                          );
                        },
                      ),
                    ],
                  )
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
