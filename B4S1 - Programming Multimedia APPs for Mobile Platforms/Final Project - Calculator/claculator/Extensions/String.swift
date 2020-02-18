extension String {
    
    func removeWhitespace() -> String {
        var string = self
        string = string.replacingOccurrences(of: " ", with: "")
        string = string.replacingOccurrences(of: "\t", with: "")
        string = string.replacingOccurrences(of: "\n", with: "")
        string = string.replacingOccurrences(of: "\r", with: "")
        return string
    }
    
}
