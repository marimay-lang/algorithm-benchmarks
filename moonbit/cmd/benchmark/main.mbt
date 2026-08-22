///|
fn main {
  let arguments = @env.args()
  if arguments.length() != 2 {
    @abort.abort(
      "usage: benchmark <insertion|heap-sort|stack|queue|min-heap|dsu|bfs|dijkstra>",
    )
  }
  let name = arguments[1]
  match @app.run(name) {
    Some(checksum) => println("\{name} \{checksum}")
    None => @abort.abort("unknown benchmark: \{name}")
  }
}
