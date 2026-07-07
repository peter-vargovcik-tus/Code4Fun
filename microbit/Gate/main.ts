input.onButtonPressed(Button.A, function () {
    code4fun.gateOpen()
})

input.onButtonPressed(Button.B, function () {
    code4fun.gateClose()
})

input.onButtonPressed(Button.AB, function () {
    if (code4fun.gateIsClosed()) {
        code4fun.gateOpen()
    } else {
        code4fun.gateClose()
    }
})
