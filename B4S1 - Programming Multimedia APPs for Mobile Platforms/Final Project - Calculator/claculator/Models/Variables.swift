class Variables {
    
    private var variables = [String: String]()
    
    func clear() {
        variables.removeAll()
    }
    
    func count() -> Int {
        return self.variables.count
    }
    
    func add(_ name: String, _ value: String) -> (String, String)? {
        var name = name.removeWhitespace()
        let value = value.removeWhitespace()
        if let _ = Float64(value) {
            name = "$" + name.replacingOccurrences(of: "$", with: "").lowercased()
            if self.variables.index(forKey: name) == nil {
                self.variables[name] = value
                return (name, value)
            }
        }
        return nil
    }
    
    func replaceToValue(_ text: String) -> String {
        var text = text
        for (name, value) in self.variables {
            text = text.replacingOccurrences(of: name, with: value)
        }
        return text
    }
    
    func describe() -> String {
        if self.variables.count == 0 {
            return ""
        }
        var description = ""
        for (name, value) in self.variables {
            description += name + "=" + value + ", "
        }
        return String(description.dropLast(2))
    }
    
}



