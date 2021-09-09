# Telemetry Demo

Just working my way through [Open Telemetry's Python Getting Started Guide](https://opentelemetry.io/docs/python/getting-started/)

Added a bit onto it.

To get up and running right away just run `docker-compose up`

## Digging Deeper

Navigat to the `telemetry_demo` directory

Start with `basic-trace-example.py` to log some trace spans to your console.

Then move on to `jaeger-export-example.py` to send those same spans to Jaeger and get a visualization. Directions are in the comments of the file.

Next take a look at `flask-instrumentation-example.py` and run it locally to export flask traces to Jaeger.

Finally, the docs get a little tricky around the collector section. I thought it was odd that they mention pushing spans from multiple services to a collector and then gave an example of pushing a single service's spans to a collector and not forwarding them on to any backend service. So, I figured it out.

Have a look at `app.py` and one of the `send-to-collector...py` files.

I've containerized all of them, as well as provided a docker-compose file to stand up each service on a virtual network (still accessible on the host machine). Ideally each of these would be in its own package and blahblahblah... whatever, this is not inteded for production. This is just me exploring OpenTelemetry because the vendor voodoo around it is probably not as complex as they advertize... In fact I think using OpenTelemetry is a better option, rolling your own instrumentation allows you/team to migrate between o11y stacks, never repeating the work. While going all in on a vendor would require you to re-write the code that helps its agent process your traces. But pretty much all the major player's agents accept OTEL traces natively. Be lazy.

`app.py` is the same flask app from earlier, but instead of pushing directly to Jaeger, it pushes traces to the collector who then pushes them to Jaeger. Same with the `send-to-collector` services. 

The compose file is all-inclusive. I suggest running `docker-compose up --scale sender=5 --scale sender2=5`. This will spawn 5 of each `send-to-collector` service (which only sends one trace then dies [one of the services sends 3 spans with different span ID's, this is intentional here but should not be done IRL]).

*Enjoy!*