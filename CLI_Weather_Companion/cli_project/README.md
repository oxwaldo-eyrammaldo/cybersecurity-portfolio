# CLI Weather Companion
#### Video Demo: [https://youtu.be/2XW2dxn0lQw]
#### Description:

The CLI Weather Companion is an interactive, command-line utility built entirely in Python that provides clean, localized, and context-aware meteorological profiles directly within a shell terminal environment. Designed specifically as a final project milestone for Harvard University's CS50P curriculum, the application leverages structural software design patterns, deep network requests processing, exception handling paradigms, and functional unit testing patterns.

### System Architecture and Functionality

The program operates by taking a plain text geographic string from standard input, dynamically generating clean uniform web API requests, sanitizing downstream payloads, and compiling metrics into a scannable structural interface.

Rather than relying on local database stores or hardcoded configurations, the core application architecture consumes real-time live web metrics by integrating seamlessly with the open-source wttr.in service layer using specialized dictionary formatting criteria.

#### project.py Breakdown
The primary application runtime is managed explicitly within `project.py` across four architectural boundaries:
1. `main()`: Orchestrates runtime lifecycle control flow. It handles initial I/O string captures, monitors exit criteria, and links parsing workers together cleanly.
2. `fetch_weather_data(city_name)`: Manages outbound HTTP client routines. Configured with rigorous explicit timeout protections, it captures raw response buffers and abstracts communication faults behind localized exceptions.
3. `extract_weather_metrics(json_data)`: Decouples incoming multi-dimensional dictionary structures. It isolates raw values safely, using robust fallback structures to handle key omissions without runtime failures.
4. `format_weather_display(city, metrics)`: Generates structured console layouts using clean visual spacing.

#### Design Choices and Tradeoffs
During the developmental phase, a significant design question emerged around selecting an underlying data API. While major production weather platforms (such as OpenWeatherMap) offer enterprise analytics parameters, they mandate localized storage schemas for unique authorization keys. To eliminate configuration complexities for final assessment grading, the application leverages wttr.in's system engine, using strict JSON parameters (`format=j1`) to bypass standard visual formats in favor of programmable dictionaries.

Additionally, standard logic blocks were deliberately isolated from state changes or network interfaces. By decoupling parsing logic (`extract_weather_metrics`) from I/O interactions (`fetch_weather_data`), the system becomes fully verifiable via isolated mock testing suites.

---

### Verification Testing Profile

The companion testing pipeline resides cleanly inside `test_project.py` and evaluates runtime components via `pytest`. The validation checks focus on input boundaries, structural missing-key resilience, and text-interface accuracy. By simulating web data payloads directly within the assertions, the testing engine runs reliably across environments without making active internet connections.
