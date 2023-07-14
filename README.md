# ApplicationInsights-Python_Flask-instrumentation-bug
Demonstrating a potential bug in how Flask is instrumented by `configure_azure_monitor`

To test:
1. Run `docker compose up`
2. Make a call to `localhost:8002/posts`
3. Review the console logs for both containers for the output `traceparent`

To test "fix":
1. Uncomment line 28 of `flask/app/__init__.py`
2. Restart the Flask container
3. Run the test again
