import 'package:flutter/material.dart';
import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key}); // Add 'const' here

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text("Flutter WebSocket Example")),
        body: WebSocketDemo(
          channel: IOWebSocketChannel.connect('ws://10.0.2.2:8000/ws'),
        ),
      ),
    );
  }
}

class WebSocketDemo extends StatefulWidget {
  final WebSocketChannel channel;

  const WebSocketDemo({super.key, required this.channel}); // Add 'const' here

  @override
  WebSocketDemoState createState() => WebSocketDemoState();
}

class WebSocketDemoState extends State<WebSocketDemo> {
  final TextEditingController _controller = TextEditingController();
  String receivedMessage = "No data yet";

  void _sendMessage() {
    if (_controller.text.isNotEmpty) {
      widget.channel.sink.add(_controller.text);
      _controller.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          TextField(
            controller: _controller,
            decoration: const InputDecoration(labelText: "Send a message"),
          ),
          const SizedBox(height: 10),
          ElevatedButton(
            onPressed: _sendMessage,
            child: const Text("Send"),
          ),
          const SizedBox(height: 20),
          const Text("Received Data:", style: TextStyle(fontWeight: FontWeight.bold)),
          StreamBuilder(
            stream: widget.channel.stream,
            builder: (context, snapshot) {
              return Text(snapshot.hasData ? snapshot.data.toString() : receivedMessage);
            },
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    widget.channel.sink.close();
    super.dispose();
  }
}
