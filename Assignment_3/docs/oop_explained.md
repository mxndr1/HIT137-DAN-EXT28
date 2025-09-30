# OOP Concepts (Simple)

- Encapsulation: Each adapter wraps its model and exposes `run()`.
- Polymorphism: Both adapters implement `run()` with different inputs.
- Multiple Inheritance: BaseAdapter inherits LoggingMixin + ValidationMixin.
- Decorators: `@requires_input` validates, `@timed` measures runtime.
