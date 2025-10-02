import 'package:flutter/material.dart';

// Importa tus pantallas
import 'package:app/screens/perfil.dart';
import 'package:app/screens/notificaciones.dart';
import 'package:app/screens/convocatorias.dart';
import 'package:app/screens/banco_uniformes.dart';
import 'package:app/screens/encuestas.dart';
import 'package:app/screens/solicitud_acompanamiento.dart';

class MenuPrincipal extends StatelessWidget {
  const MenuPrincipal({super.key});

  // Lista de opciones con su ruta
  final List<Map<String, dynamic>> menuOptions = const [
    {"title": "Perfil", "icon": Icons.person, "enabled": true, "route": PerfilScreen()},
    {"title": "Notificaciones", "icon": Icons.notifications, "enabled": true, "route": NotificacionesScreen()},
    {"title": "Convocatorias", "icon": Icons.campaign, "enabled": true, "route": ConvocatoriasScreen()},
    {"title": "Banco de uniformes", "icon": Icons.checkroom, "enabled": true, "route": BancoUniformesScreen()},
    {"title": "Encuestas", "icon": Icons.poll, "enabled": true, "route": EncuestasScreen()},
    {"title": "Solicitar acompañamiento", "icon": Icons.support, "enabled": true, "route": SolicitudAcompanamientoScreen()},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Menú Principal"),
        backgroundColor: Colors.green[700],
        elevation: 5,
      ),

      // Drawer tipo hamburguesa
      drawer: Drawer(
        child: Column(
          children: [
            DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.green[700],
              ),
              child: const Align(
                alignment: Alignment.bottomLeft,
                child: Text(
                  "Bienvenido Aprendiz",
                  style: TextStyle(
                    fontSize: 22,
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: menuOptions.length,
                itemBuilder: (context, index) {
                  final option = menuOptions[index];

                  return ListTile(
                    leading: Icon(
                      option["icon"],
                      color: option["enabled"]
                          ? Colors.green[700]
                          : Colors.grey,
                    ),
                    title: Text(
                      option["title"],
                      style: TextStyle(
                        color: option["enabled"]
                            ? Colors.black
                            : Colors.grey,
                      ),
                    ),
                    trailing: option["enabled"]
                        ? const Icon(Icons.arrow_forward_ios, size: 16)
                        : const Icon(Icons.lock, color: Colors.grey),
                    onTap: option["enabled"]
                        ? () {
                            Navigator.pop(context); // cerrar drawer
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => option["route"],
                              ),
                            );
                          }
                        : null,
                  );
                },
              ),
            ),
          ],
        ),
      ),

      // Espacio principal para gráficas
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Center(
          child: Container(
            width: double.infinity,
            decoration: BoxDecoration(
              color: Colors.grey[200],
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.green.shade700, width: 2),
            ),
            child: const Center(
              child: Text(
                "AQUI APARECERÁ TU PROCESO ",
                style: TextStyle(fontSize: 16, color: Colors.black54),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
