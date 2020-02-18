import Foundation

class History {
    
    let formula: String
    let variables: Variables
    let result: Float64
    var isLocked: Bool
    
    init(_ formula: String, _ variables: Variables, _ result: Float64) {
        self.formula = formula
        self.variables = variables
        self.result = result
        self.isLocked = false
    }
    
    func lock() {
        self.isLocked = true
    }
    
    func unlock() {
        self.isLocked = false
    }
    
}

func getDateString() -> String {
    let dateFormatter = DateFormatter()
    dateFormatter.dateFormat = "yyyy/MM/dd"
    return dateFormatter.string(from: Date())
}

class Histories {
    
    private var dates = [String]()
    private var histories = [[History]]()
    
    func countOfDates() -> Int {
        return self.dates.count
    }
    
    func countAtDateIndex(_ dateIndex: Int) -> Int {
        if dateIndex >= self.histories.count {
            return 0
        }
        return self.histories[dateIndex].count
    }
    
    func getDateByIndex(_ dateIndex: Int) -> String {
        return self.dates[dateIndex]
    }
    
    func get(_ dateIndex: Int, _ id: Int) -> (String, History)? {
        if dateIndex < self.dates.count && id < self.histories[dateIndex].count {
            return (self.dates[dateIndex], self.histories[dateIndex][id])
        }
        return nil
    }
    
    func add(_ history: History, _ date: String = "") {
        var date = date
        if date == "" {
            date = getDateString()
            history.isLocked = false
        } else {
            history.isLocked = true
        }
        var dateIndex = self.dates.count
        if let di = self.dates.firstIndex(of: date) {
            dateIndex = di
        } else {
            self.dates.append(date)
            self.histories.append([History]())
        }
        self.histories[dateIndex].append(history)
    }
    
    func delete(_ dateIndex: Int, _ id: Int) -> Bool {
        if dateIndex >= self.dates.count || id >= self.histories[dateIndex].count {
            return false
        }
        self.histories[dateIndex].remove(at: id)
        if self.histories[dateIndex].count == 0 {
            self.dates.remove(at: dateIndex)
            self.histories.remove(at: dateIndex)
        }
        print(self.dates.count)
        return true
    }
    
    func clear() {
        let newHistories = Histories()
        for i in 0..<self.dates.count {
            for h in self.histories[i] {
                if h.isLocked {
                    newHistories.add(h, self.dates[i])
                }
            }
        }
        self.histories = newHistories.histories
        self.dates = newHistories.dates
    }
    
}

var histories = Histories()
