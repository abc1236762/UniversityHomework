import UIKit

class HistoryTableViewController: UITableViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.navigationItem.leftBarButtonItem = UIBarButtonItem(barButtonSystemItem: .trash, target: self, action: #selector(self.leftBarButtonItemAction(sender:)))
        self.navigationItem.rightBarButtonItem = UIBarButtonItem(barButtonSystemItem: .refresh, target: self, action: #selector(self.rightBarButtonItemAction(sender:)))
        NotificationCenter.default.addObserver(self, selector: #selector(self.updateHistory), name: NSNotification.Name(rawValue: "updateHistory"), object: nil)
    }
    
    override func numberOfSections(in tableView: UITableView) -> Int {
        return histories.countOfDates()
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return histories.countAtDateIndex(section)
    }
    
    override func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return histories.getDateByIndex(section)
    }
    
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: false)
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "history", for: indexPath)
        let (_, history) = histories.get(indexPath.section, indexPath.row)!
        cell.textLabel?.text = history.formula
        if history.variables.count() > 0 {
            cell.textLabel?.text! += ", with " +  history.variables.describe()
        }
        cell.detailTextLabel?.text = String(history.result)
        if history.isLocked {
            cell.contentView.backgroundColor = .yellow
        }
        return cell
    }
    
    override func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCell.EditingStyle, forRowAt indexPath: IndexPath) {
        if editingStyle == .delete {
            if histories.delete(indexPath.section, indexPath.row) {
                if histories.countAtDateIndex(indexPath.section) == 0 {
                    tableView.deleteSections([indexPath.section], with: .fade)
                } else {
                    tableView.deleteRows(at: [indexPath], with: .fade)
                }
            }
        }
    }
    
    override func tableView(_ tableView: UITableView, leadingSwipeActionsConfigurationForRowAt indexPath: IndexPath) -> UISwipeActionsConfiguration? {
        let cell = tableView.dequeueReusableCell(withIdentifier: "history", for: indexPath)
        let (_, history) = histories.get(indexPath.section, indexPath.row)!
        let title = history.isLocked ? "Unlock" : "Lock"
        let action = UIContextualAction(style: .normal, title: title) { (action, view, handler) in
            if history.isLocked {
                history.unlock()
                cell.backgroundColor = .none
            } else {
                history.lock()
                cell.backgroundColor = .yellow
            }
            handler(true)
        }
        return UISwipeActionsConfiguration(actions: [action])
    }
    
    @objc func leftBarButtonItemAction(sender: UIBarButtonItem) {
        histories.clear()
        self.updateHistory()
    }
    
    @objc func rightBarButtonItemAction(sender: UIBarButtonItem) {
        self.updateHistory()
    }
    
    @objc func updateHistory() {
        self.tableView.reloadData()
    }
    
}
