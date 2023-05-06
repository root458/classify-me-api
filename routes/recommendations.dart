import 'package:dart_frog/dart_frog.dart';

Response onRequest(RequestContext context) {
  return Response.json(
    body: {
      'first': 'Nursing',
      'second': 'Pharmacy',
      'third': 'Medicine',
    },
  );
}
