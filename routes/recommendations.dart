import 'package:dart_frog/dart_frog.dart';

Response onRequest(RequestContext context) {
  // Access the incoming request.
  final request = context.request;

  // Access the query parameters as a `Map<String, String>`.
  // ignore: unused_local_variable
  final params = request.uri.queryParameters;

  return Response.json(
    body: {
      'first': 'Nursing',
      'second': 'Pharmacy',
      'third': 'Medicine',
    },
  );
}
