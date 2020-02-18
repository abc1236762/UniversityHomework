import UIKit

class ClaculatorViewController: UIViewController, UITableViewDataSource, UITableViewDelegate,  UIPickerViewDataSource, UIPickerViewDelegate {
    
    @IBOutlet var formulaTextField: UITextField!
    @IBOutlet var resultLabel: UILabel!
    @IBOutlet var variablesTableView: UITableView!
    @IBOutlet var functionsPickerView: UIPickerView!
    
    var function = functions[0]
    var variables = Variables()
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 8
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        return tableView.dequeueReusableCell(withIdentifier: "variable", for: indexPath)
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: false)
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return functions.count
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return functions[row].name
    }
    
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        self.function = functions[row]
    }
    
    @IBAction func UpdateVariablesButtonTouchUpInside(_ sender: UIButton) {
        self.variables.clear()
        for cell in variablesTableView.visibleCells {
            let cell = cell as! VariableTableViewCell
            let name = cell.nameTextField.text ?? ""
            let value = cell.valueTextField.text ?? ""
            if let (name, value) = self.variables.add(name, value) {
                cell.nameTextField.text = name
                cell.valueTextField.text = value
            } else {
                cell.nameTextField.text = ""
                cell.valueTextField.text = ""
            }
        }
    }
    
    @IBAction func applyButtonTouchUpInside(_ sender: UIButton) {
        var text = formulaTextField.text ?? ""
        if let selectedRange = formulaTextField.selectedTextRange {
            var pos = formulaTextField.offset(from: formulaTextField.beginningOfDocument, to: selectedRange.start)
            (text, pos) = insertFunctionInText(text, pos, self.function)
            formulaTextField.text = text
            if let newPosition = formulaTextField.position(from: formulaTextField.beginningOfDocument, offset: pos) {
                formulaTextField.selectedTextRange = formulaTextField.textRange(from: newPosition, to: newPosition)
            }
        }
        formulaTextFieldEditingChanged(formulaTextField)
    }
    
    @IBAction func formulaTextFieldEditingChanged(_ sender: UITextField) {
        let text = formulaTextField.text ?? ""
        let script = compileTextToScript(text, self.variables)
        if script.isEmpty {
            resultLabel.text = "input something…"
        } else {
            if let result = calculateScript(script) {
                resultLabel.text = String(result)
                histories.add(History(text, variables, result))
                NotificationCenter.default.post(name: NSNotification.Name(rawValue: "updateHistory"), object: nil)
            } else {
                resultLabel.text = "syntax error"
            }
        }
    }

}
