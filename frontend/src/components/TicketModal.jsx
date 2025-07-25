"use client"

const TicketModal = ({ ticket, onClose }) => {
  if (!ticket) return null

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  const getStatusBadge = (status) => {
    const statusClasses = {
      open: "bg-green-100 text-green-800",
      "in-progress": "bg-yellow-100 text-yellow-800",
      closed: "bg-gray-100 text-gray-800",
    }

    return (
      <span
        className={`px-3 py-1 text-sm font-medium rounded-full ${statusClasses[status] || "bg-gray-100 text-gray-800"}`}
      >
        {status}
      </span>
    )
  }

  const getPriorityBadge = (priority) => {
    const priorityClasses = {
      high: "bg-red-100 text-red-800",
      medium: "bg-orange-100 text-orange-800",
      low: "bg-blue-100 text-blue-800",
    }

    return (
      <span
        className={`px-3 py-1 text-sm font-medium rounded-full ${priorityClasses[priority] || "bg-gray-100 text-gray-800"}`}
      >
        {priority}
      </span>
    )
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-200">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Ticket #{ticket.id}</h2>
              <div className="flex items-center space-x-3">
                {getStatusBadge(ticket.status)}
                {getPriorityBadge(ticket.priority)}
              </div>
            </div>
            <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-2xl font-bold">
              ×
            </button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Subject</h3>
            <p className="text-gray-700">{ticket.subject}</p>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-gray-700 whitespace-pre-wrap">{ticket.body}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Customer Information</h3>
              <div className="space-y-2">
                <p>
                  <span className="font-medium">Name:</span> {ticket.customer_name}
                </p>
                <p>
                  <span className="font-medium">Email:</span> {ticket.customer_email}
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Ticket Details</h3>
              <div className="space-y-2">
                <p>
                  <span className="font-medium">Assigned Agent:</span> {ticket.assigned_agent || "Unassigned"}
                </p>
                <p>
                  <span className="font-medium">Created:</span> {formatDate(ticket.created_at)}
                </p>
                <p>
                  <span className="font-medium">Updated:</span> {formatDate(ticket.updated_at)}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 border-t border-gray-200">
          <button
            onClick={onClose}
            className="w-full bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

export default TicketModal
