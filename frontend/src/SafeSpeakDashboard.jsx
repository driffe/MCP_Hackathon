import { useState, useEffect } from "react";
import { Bell, BrainCircuit, Clock, Globe, Menu, X, User, Settings, Home, AlertCircle, CheckCircle } from "lucide-react";

// Dashboard component
export default function SafeSpeakDashboard() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [alert, setAlert] = useState(null);
  
  // Sample user data
  const user = {
    name: "David Chen",
    status: "Safe",
    lastActive: "2 minutes ago",
    emotionalStatus: "Stable",
    routineStatus: "Normal",
    emergencyContacts: [
      { name: "Sarah Chen", relationship: "Daughter", phone: "+1-555-123-4567" },
      { name: "Local Care Center", relationship: "Care Provider", phone: "+1-555-987-6543" }
    ]
  };

  // Sample alert history
  const [alertHistory, setAlertHistory] = useState([
    { 
      id: 1, 
      type: "emotional", 
      timestamp: "2025-05-01T18:32:00", 
      description: "Detected signs of depression in speech patterns", 
      status: "Resolved", 
      action: "Auto-notification sent to Sarah Chen" 
    },
    { 
      id: 2, 
      type: "routine", 
      timestamp: "2025-04-29T09:15:00", 
      description: "No movement detected for 12 hours", 
      status: "Resolved", 
      action: "False alarm - user responded to notification" 
    },
    { 
      id: 3, 
      type: "medication", 
      timestamp: "2025-04-27T21:00:00", 
      description: "Evening medication not taken", 
      status: "Resolved", 
      action: "User took medication after reminder" 
    }
  ]);

  // Demo for showing an alert
  useEffect(() => {
    const timer = setTimeout(() => {
      setAlert({
        message: "Emotional distress detected. Monitoring increased.",
        type: "warning"
      });
      
      // Clear alert after 5 seconds
      setTimeout(() => setAlert(null), 5000);
    }, 3000);
    
    return () => clearTimeout(timer);
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
      hour12: true
    });
  };

  // Features for the dashboard page
  const features = [
    {
      title: "Emotional Change Detection",
      icon: <BrainCircuit className="w-6 h-6" />,
      description: "Analyzes speech patterns and vocal tone to detect signs of depression or emotional distress",
      status: "Active",
      lastCheck: "2 minutes ago"
    },
    {
      title: "Abnormal Routine Detection",
      icon: <Clock className="w-6 h-6" />,
      description: "Monitors daily activities to identify disrupted routines or unusual behaviors",
      status: "Active", 
      lastCheck: "15 minutes ago"
    },
    {
      title: "Emergency Auto Alerts",
      icon: <Bell className="w-6 h-6" />,
      description: "Automatically notifies caregivers or authorities when danger conditions are detected",
      status: "Active",
      lastCheck: "2 minutes ago"
    },
    {
      title: "Multilingual Safety Alerts",
      icon: <Globe className="w-6 h-6" />,
      description: "Sends emergency messages in the preferred language of each emergency contact",
      status: "Active",
      lastCheck: "2 minutes ago"
    }
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}
      
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-30 w-64 bg-indigo-800 text-white transform transition-transform duration-200 ease-in-out lg:translate-x-0 lg:static lg:block ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="p-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">SafeSpeak</h1>
          <button onClick={() => setSidebarOpen(false)} className="lg:hidden">
            <X className="w-6 h-6" />
          </button>
        </div>
        <div className="p-4">
          <div className="flex items-center space-x-3 p-3 mb-6 bg-indigo-700 rounded-lg">
            <User className="w-8 h-8" />
            <div>
              <div className="font-medium">{user.name}</div>
              <div className="text-sm text-indigo-200">Status: {user.status}</div>
            </div>
          </div>
          <nav className="space-y-1">
            <button 
              onClick={() => setActiveTab("dashboard")}
              className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-colors ${activeTab === "dashboard" ? 'bg-indigo-900' : 'hover:bg-indigo-700'}`}
            >
              <Home className="w-5 h-5" />
              <span>Dashboard</span>
            </button>
            <button 
              onClick={() => setActiveTab("alerts")}
              className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-colors ${activeTab === "alerts" ? 'bg-indigo-900' : 'hover:bg-indigo-700'}`}
            >
              <AlertCircle className="w-5 h-5" />
              <span>Alert History</span>
            </button>
            <button 
              onClick={() => setActiveTab("settings")}
              className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-colors ${activeTab === "settings" ? 'bg-indigo-900' : 'hover:bg-indigo-700'}`}
            >
              <Settings className="w-5 h-5" />
              <span>Settings</span>
            </button>
          </nav>
        </div>
      </div>
      
      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top navbar */}
        <header className="bg-white shadow-sm">
          <div className="flex items-center justify-between p-4">
            <button onClick={() => setSidebarOpen(true)} className="block lg:hidden">
              <Menu className="w-6 h-6" />
            </button>
            <div className="text-xl font-semibold text-gray-800 lg:hidden">SafeSpeak</div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Last active: {user.lastActive}</span>
            </div>
          </div>
          
          {/* Alert notification */}
          {alert && (
            <div className={`p-3 text-white ${alert.type === "warning" ? "bg-yellow-500" : alert.type === "danger" ? "bg-red-500" : "bg-green-500"}`}>
              <div className="container mx-auto flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="w-5 h-5" />
                  <span>{alert.message}</span>
                </div>
                <button onClick={() => setAlert(null)}>
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}
        </header>
        
        {/* Main content area */}
        <main className="flex-1 overflow-y-auto p-4">
          {activeTab === "dashboard" && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-gray-900">Emotional Status</h3>
                    <BrainCircuit className="w-6 h-6 text-indigo-600" />
                  </div>
                  <div className="mt-4">
                    <div className="text-2xl font-semibold text-gray-900">{user.emotionalStatus}</div>
                    <div className="text-sm text-gray-500">Last updated 2 minutes ago</div>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-gray-900">Routine Status</h3>
                    <Clock className="w-6 h-6 text-indigo-600" />
                  </div>
                  <div className="mt-4">
                    <div className="text-2xl font-semibold text-gray-900">{user.routineStatus}</div>
                    <div className="text-sm text-gray-500">Last checked 15 minutes ago</div>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-gray-900">Alert Status</h3>
                    <Bell className="w-6 h-6 text-indigo-600" />
                  </div>
                  <div className="mt-4">
                    <div className="text-2xl font-semibold text-gray-900">No active alerts</div>
                    <div className="text-sm text-gray-500">All systems normal</div>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-gray-900">Primary Contact</h3>
                    <User className="w-6 h-6 text-indigo-600" />
                  </div>
                  <div className="mt-4">
                    <div className="text-xl font-semibold text-gray-900">{user.emergencyContacts[0].name}</div>
                    <div className="text-sm text-gray-500">{user.emergencyContacts[0].phone}</div>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow">
                <div className="p-6">
                  <h2 className="text-lg font-medium text-gray-900">SafeSpeak Features</h2>
                  <p className="mt-1 text-sm text-gray-500">All features are working properly and actively monitoring</p>
                </div>
                <div className="border-t border-gray-200">
                  {features.map((feature, index) => (
                    <div key={index} className="p-6 border-b border-gray-200 last:border-b-0">
                      <div className="flex items-start">
                        <div className="flex-shrink-0 text-indigo-600">
                          {feature.icon}
                        </div>
                        <div className="ml-4">
                          <div className="flex items-center">
                            <h3 className="text-lg font-medium text-gray-900">{feature.title}</h3>
                            <span className="ml-2 px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">{feature.status}</span>
                          </div>
                          <p className="mt-1 text-sm text-gray-500">{feature.description}</p>
                          <p className="mt-2 text-xs text-gray-400">Last check: {feature.lastCheck}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
          
          {activeTab === "alerts" && (
            <div className="bg-white rounded-lg shadow">
              <div className="p-6">
                <h2 className="text-lg font-medium text-gray-900">Alert History</h2>
                <p className="mt-1 text-sm text-gray-500">Recent alerts and responses</p>
              </div>
              <div className="border-t border-gray-200">
                {alertHistory.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date & Time</th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action Taken</th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {alertHistory.map((alert) => (
                          <tr key={alert.id}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatDate(alert.timestamp)}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize">{alert.type}</td>
                            <td className="px-6 py-4 text-sm text-gray-500">{alert.description}</td>
                            <td className="px-6 py-4 text-sm text-gray-500">{alert.action}</td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 text-xs rounded-full ${alert.status === "Resolved" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}`}>
                                {alert.status}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="p-6 text-center text-gray-500">No alert history available</div>
                )}
              </div>
            </div>
          )}
          
          {activeTab === "settings" && (
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow">
                <div className="p-6">
                  <h2 className="text-lg font-medium text-gray-900">User Profile</h2>
                  <p className="mt-1 text-sm text-gray-500">Manage user information and preferences</p>
                </div>
                <div className="border-t border-gray-200 p-6">
                  <div className="grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-4">
                    <div>
                      <label htmlFor="name" className="block text-sm font-medium text-gray-700">Full Name</label>
                      <input type="text" id="name" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" defaultValue={user.name} />
                    </div>
                    <div>
                      <label htmlFor="phone" className="block text-sm font-medium text-gray-700">Phone Number</label>
                      <input type="text" id="phone" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" defaultValue="+1-555-765-4321" />
                    </div>
                    <div>
                      <label htmlFor="language" className="block text-sm font-medium text-gray-700">Preferred Language</label>
                      <select id="language" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                        <option>English</option>
                        <option>Spanish</option>
                        <option>Chinese (Mandarin)</option>
                        <option>Japanese</option>
                        <option>Korean</option>
                        <option>French</option>
                        <option>German</option>
                      </select>
                    </div>
                    <div>
                      <label htmlFor="timezone" className="block text-sm font-medium text-gray-700">Timezone</label>
                      <select id="timezone" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                        <option>Pacific Time (UTC-08:00)</option>
                        <option>Mountain Time (UTC-07:00)</option>
                        <option>Central Time (UTC-06:00)</option>
                        <option>Eastern Time (UTC-05:00)</option>
                        <option>Japan Standard Time (UTC+09:00)</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow">
                <div className="p-6">
                  <h2 className="text-lg font-medium text-gray-900">Emergency Contacts</h2>
                  <p className="mt-1 text-sm text-gray-500">People to notify in case of emergency</p>
                </div>
                <div className="border-t border-gray-200">
                  {user.emergencyContacts.map((contact, index) => (
                    <div key={index} className="p-6 border-b border-gray-200 last:border-b-0">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-sm font-medium text-gray-900">{contact.name}</h3>
                          <p className="text-sm text-gray-500">{contact.relationship}</p>
                          <p className="text-sm text-gray-500">{contact.phone}</p>
                        </div>
                        <div className="flex space-x-2">
                          <button className="p-2 text-sm text-indigo-600 hover:text-indigo-900">Edit</button>
                          <button className="p-2 text-sm text-red-600 hover:text-red-900">Remove</button>
                        </div>
                      </div>
                    </div>
                  ))}
                  <div className="p-6">
                    <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                      Add New Contact
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow">
                <div className="p-6">
                  <h2 className="text-lg font-medium text-gray-900">System Settings</h2>
                  <p className="mt-1 text-sm text-gray-500">Configure monitoring preferences</p>
                </div>
                <div className="border-t border-gray-200 p-6">
                  <div className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">Emotional Analysis Sensitivity</h3>
                        <p className="text-sm text-gray-500">Adjust how sensitive the system is to emotional changes</p>
                      </div>
                      <select className="block w-32 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                        <option>Low</option>
                        <option>Medium</option>
                        <option selected>High</option>
                      </select>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">Routine Detection Threshold</h3>
                        <p className="text-sm text-gray-500">How long before unusual inactivity triggers an alert</p>
                      </div>
                      <select className="block w-32 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                        <option>6 hours</option>
                        <option selected>12 hours</option>
                        <option>24 hours</option>
                      </select>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">Alert Confirmation</h3>
                        <p className="text-sm text-gray-500">Require confirmation before sending emergency alerts</p>
                      </div>
                      <div className="flex items-center">
                        <input type="checkbox" id="alertConfirmation" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" defaultChecked />
                        <label htmlFor="alertConfirmation" className="ml-2 text-sm text-gray-700">Enabled</label>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">Voice Monitoring Schedule</h3>
                        <p className="text-sm text-gray-500">When to actively monitor for emotional changes</p>
                      </div>
                      <select className="block w-32 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                        <option>Morning</option>
                        <option>Evening</option>
                        <option selected>All Day</option>
                        <option>Custom</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="flex justify-end space-x-3 py-4">
                <button className="px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                  Cancel
                </button>
                <button className="px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                  Save Settings
                </button>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}