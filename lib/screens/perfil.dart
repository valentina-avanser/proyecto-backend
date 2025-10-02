import 'package:flutter/material.dart';

class PerfilScreen extends StatefulWidget {
  const PerfilScreen({super.key});

  @override
  State<PerfilScreen> createState() => _PerfilScreenState();
}

class _PerfilScreenState extends State<PerfilScreen> {
  // Controladores con tus datos precargados
  final TextEditingController nombresCtrl =
      TextEditingController(text: "Daniel Felipe");
  final TextEditingController apellidosCtrl =
      TextEditingController(text: "Pérez Burbano");
  final TextEditingController fechaNacimientoCtrl =
      TextEditingController(text: "12/11/2005");
  final TextEditingController tipoDocCtrl =
      TextEditingController(text: "Cédula de Ciudadanía");
  final TextEditingController numeroDocCtrl =
      TextEditingController(text: "1058965246");
  final TextEditingController correoCtrl =
      TextEditingController(text: "danielfelipeperezbbn@gmail.com");
  final TextEditingController celularCtrl =
      TextEditingController(text: "3103014544");
  final TextEditingController estratoCtrl =
      TextEditingController(text: "1");
  final TextEditingController ciudadCtrl =
      TextEditingController(text: "Popayán");
  final TextEditingController direccionCtrl =
      TextEditingController(text: "Colinas de Calicanto manzana D#10");

  bool datosModificados = false; // Para mostrar el botón de actualizar

  void marcarModificado() {
    setState(() {
      datosModificados = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Perfil del Aprendiz"),
        backgroundColor: Colors.green[700],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            // Foto de perfil
            Center(
              child: CircleAvatar(
                radius: 50,
                backgroundColor: Colors.green[200],
                child: const Icon(Icons.person, size: 60, color: Colors.white),
              ),
            ),
            const SizedBox(height: 20),

            // Campos de formulario
            _campo("Nombres", nombresCtrl),
            _campo("Apellidos", apellidosCtrl),
            _campo("Fecha de nacimiento", fechaNacimientoCtrl, esFecha: true),
            _campo("Tipo de documento", tipoDocCtrl),
            _campo("Número de documento", numeroDocCtrl),
            _campo("Correo", correoCtrl, tipo: TextInputType.emailAddress),
            _campo("Celular", celularCtrl, tipo: TextInputType.phone),
            _campo("Estrato socioeconómico", estratoCtrl, tipo: TextInputType.number),
            _campo("Ciudad/Municipio", ciudadCtrl),
            _campo("Dirección", direccionCtrl),

            const SizedBox(height: 20),

            if (datosModificados)
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green[700],
                  padding: const EdgeInsets.symmetric(vertical: 15),
                ),
                icon: const Icon(Icons.save, color: Colors.white),
                label: const Text(
                  "Actualizar",
                  style: TextStyle(fontSize: 18, color: Colors.white),
                ),
                onPressed: () {
                  setState(() {
                    datosModificados = false;
                  });
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text("Perfil actualizado ✅")),
                  );
                },
              ),
          ],
        ),
      ),
    );
  }

  Widget _campo(String label, TextEditingController controller,
      {bool esFecha = false, TextInputType tipo = TextInputType.text}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: TextFormField(
        controller: controller,
        keyboardType: tipo,
        readOnly: esFecha,
        decoration: InputDecoration(
          labelText: label,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          suffixIcon: esFecha ? const Icon(Icons.calendar_today) : null,
        ),
        onChanged: (_) => marcarModificado(),
        onTap: esFecha
            ? () async {
                DateTime? pickedDate = await showDatePicker(
                  context: context,
                  initialDate: DateTime(2005, 11, 12),
                  firstDate: DateTime(1900),
                  lastDate: DateTime.now(),
                );
                if (pickedDate != null) {
                  controller.text =
                      "${pickedDate.day}/${pickedDate.month}/${pickedDate.year}";
                  marcarModificado();
                }
              }
            : null,
      ),
    );
  }
}
