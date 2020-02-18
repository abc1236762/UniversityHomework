import JavaScriptCore

struct Function {
    
    let name: String
    let text: String
    let script: String
    let args: String
    
    init(_ name: String, _ text: String, _ script: String, _ args: String) {
        self.name = name
        self.text = text
        self.script = script
        self.args = args
    }
    
}

let functions = [
    Function("𝑒", "E", "Math.E", ""),
    Function("π", "Pi", "Math.PI", ""),
    Function("|𝑥|", "Abs", "Math.abs", "$x"),
    Function("⌈𝑥⌉", "Ceil", "Math.ceil", "$x"),
    Function("⌊𝑥⌋", "Floor", "Math.floor", "$x"),
    Function("round", "Round", "Math.round", "$x"),
    Function("max", "Max", "Math.max", "…"),
    Function("min", "Min", "Math.min", "…"),
    Function("𝑒ⁱ", "Exp", "Math.exp", "$i"),
    Function("logₑ", "Log", "Math.log", "$x"),
    Function("log₂", "Log2", "Math.log2", "$x"),
    Function("log₁₀", "Log10", "Math.log10", "$x"),
    Function("𝑥ⁱ", "Pow", "Math.pow", "$x,$i"),
    Function("𝑥²", "Sqrt", "Math.sqrt", "$x"),
    Function("𝑥³", "Cbrt", "Math.cbrt", "$x"),
    Function("sin", "Sin", "Math.sin", "$x"),
    Function("cos", "Cos", "Math.cos", "$x"),
    Function("tan", "Tan", "Math.tan", "$x"),
    Function("sin⁻¹", "Asin", "Math.asin", "$x"),
    Function("cos⁻¹", "Acos", "Math.acos", "$x"),
    Function("tan⁻¹", "Atan", "Math.atan", "$x"),
    Function("sinh", "Sinh", "Math.sinh", "$x"),
    Function("cosh", "Cosh", "Math.cosh", "$x"),
    Function("tanh", "Tanh", "Math.tanh", "$x"),
    Function("sinh⁻¹", "Asinh", "Math.asinh", "$x"),
    Function("cosh⁻¹", "Acosh", "Math.acosh", "$x"),
    Function("tanh⁻¹", "Atanh", "Math.atanh", "$x"),
]

func insertFunctionInText(_ text: String, _ pos: Int, _ function: Function) -> (String, Int) {
    var text = text
    let content = function.text + "(" + function.args + ")"
    text.insert(contentsOf: content, at: text.index(text.startIndex, offsetBy: pos))
    var pos = pos + content.count
    if !function.args.isEmpty {
        pos += 1
    }
    return (text, pos)
}

func compileTextToScript(_ text: String, _ variables: Variables) -> String {
    var script = text.removeWhitespace()
    for function in functions {
        if function.args.isEmpty {
            script = script.replacingOccurrences(of: function.text + "()", with: function.script)
        } else {
            script = script.replacingOccurrences(of: function.text + "(", with: function.script + "(")
        }
    }
    script = variables.replaceToValue(script)
    return script
}

func calculateScript(_ script: String) -> Float64? {
    if let result = JSContext()?.evaluateScript(script)?.toString() {
        if let value = Float64(result) {
            return value
        }
    }
    return nil
}
