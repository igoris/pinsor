#explanation of how to use fluent interface

# Introduction #

The fluent interface is a good way to register several Components at once, this is feature equivalent with AddComponent and preference is the only factor.

# Samples #

Basic Registration

```python


pinsor = !PinsorContainer()
pinsor.register(
Component.oftype(!FakeObj)
)

```

Registers Dependencies

```python


pinsor = !PinsorContainer()
pinsor.register(
Component.oftype(!FakeObj),
Component.oftype(!NeedsFakeObj).depends([FakeObj])
)

```

Sets component lifestyle

```python


pinsor = !PinsorContainer()
pinsor.register(
Component.oftype(!FakeObj).lifestyle(!LifeStyle.transient())
)

```

Sets key so you can register several at once

```python


pinsor = !PinsorContainer()
pinsor.register(
Component.oftype(!FakeObj).named("fake1"),
Component.oftype(!FakeObj).named("fake2")
)

```

Set up several options at once

```python


pinsor = !PinsorContainer()
pinsor.register(
Component.oftype(!FakeObj),
Component.oftype(!NeedsFakeObj).depends([FakeObj]).lifestyle(!LifeStyle.transient()).named("needs")
)

```