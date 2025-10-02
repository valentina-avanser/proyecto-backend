import 'package:flutter/material.dart';

class SolicitudAcompanamientoScreen extends StatefulWidget {
  const SolicitudAcompanamientoScreen({super.key});

  @override
  State<SolicitudAcompanamientoScreen> createState() =>
      _SolicitudAcompanamientoScreenState();
}

class _SolicitudAcompanamientoScreenState
    extends State<SolicitudAcompanamientoScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _motivoController = TextEditingController();

  DateTime? _fechaSeleccionada;
  TimeOfDay? _horaSeleccionada;

  // Método para seleccionar fecha
  Future<void> _seleccionarFecha(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(), // No permite fechas pasadas
      lastDate: DateTime(2100),
    );
    if (picked != null && picked != _fechaSeleccionada) {
      setState(() {
        _fechaSeleccionada = picked;
      });
    }
  }

  // Método para seleccionar hora
  Future<void> _seleccionarHora(BuildContext context) async {
    final TimeOfDay? picked =
        await showTimePicker(context: context, initialTime: TimeOfDay.now());
    if (picked != null && picked != _horaSeleccionada) {
      setState(() {
        _horaSeleccionada = picked;
      });
    }
  }

  void _enviarSolicitud() {
    if (_formKey.currentState!.validate() &&
        _fechaSeleccionada != null &&
        _horaSeleccionada != null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            "✅ Solicitud enviada\n"
            "Motivo: ${_motivoController.text}\n"
            "Día: ${_fechaSeleccionada!.day}/${_fechaSeleccionada!.month}/${_fechaSeleccionada!.year}\n"
            "Hora: ${_horaSeleccionada!.format(context)}",
          ),
          duration: const Duration(seconds: 4),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("⚠️ Completa todos los campos antes de enviar."),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Solicitud de Acompañamiento"),
        backgroundColor: Colors.green[700],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Motivo
              TextFormField(
                controller: _motivoController,
                decoration: const InputDecoration(
                  labelText: "Motivo de la solicitud",
                  border: OutlineInputBorder(),
                  helperText: "Ejemplo: orientación académica, apoyo personal, etc.",
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return "Por favor ingresa el motivo.";
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),

              // Selección de fecha
              ListTile(
                leading: const Icon(Icons.calendar_today, color: Colors.green),
                title: Text(
                  _fechaSeleccionada == null
                      ? "Seleccionar día"
                      : "Día: ${_fechaSeleccionada!.day}/${_fechaSeleccionada!.month}/${_fechaSeleccionada!.year}",
                ),
                onTap: () => _seleccionarFecha(context),
              ),

              // Selección de hora
              ListTile(
                leading: const Icon(Icons.access_time, color: Colors.green),
                title: Text(
                  _horaSeleccionada == null
                      ? "Seleccionar hora"
                      : "Hora: ${_horaSeleccionada!.format(context)}",
                ),
                onTap: () => _seleccionarHora(context),
              ),
              const SizedBox(height: 20),

              // Botón enviar
              Center(
                child: ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green[700],
                    padding: const EdgeInsets.symmetric(
                        horizontal: 24, vertical: 12),
                  ),
                  icon: const Icon(Icons.send, color: Colors.white),
                  label: const Text(
                    "Solicitar cita",
                    style: TextStyle(color: Colors.white, fontSize: 16),
                  ),
                  onPressed: _enviarSolicitud,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
