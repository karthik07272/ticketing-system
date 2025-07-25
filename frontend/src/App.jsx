"use client"

import { useState, useRef, useEffect } from "react"
import TicketTable from "./components/TicketTable"
import SearchFilters from "./components/SearchFilters"
import TicketModal from "./components/TicketModal"
import CreateTicketModal from "./components/CreateTicketModal"
import { ticketService } from "./services/ticketService"


function App() {
  const [tickets, setTickets] = useState([])
  const [loading, setLoading] = useState(false)
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 20,
    totalCount: 0,
    totalPages: 0,
    hasNext: false,
    hasPrev: false,
  })

  const [filters, setFilters] = useState({
    search: "",
    status: "",
    priority: "",
    dateFrom: "",
    dateTo: "",
  })

  const [selectedTicket, setSelectedTicket] = useState(null)
  const [showTicketModal, setShowTicketModal] = useState(false)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editingTicket, setEditingTicket] = useState(null)


  useEffect(() => {
    fetchTickets()
  }, [])

  const fetchTickets = async (page = 1, newFilters = filters) => {
    setLoading(true)
    try {
      const response = await ticketService.searchTickets({
        page,
        pageSize: pagination.pageSize,
        ...newFilters,
      })

      setTickets(response.tickets)
      setPagination({
        page: response.page,
        pageSize: response.page_size,
        totalCount: response.total_count,
        totalPages: response.total_pages,
        hasNext: response.has_next,
        hasPrev: response.has_prev,
      })
    } catch (error) {
      console.error("Error fetching tickets:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleSeedDatabase = async () => {
    if (!window.confirm("Are you sure you want to seed 100,000 tickets? This may take a few seconds.")) return

    try {
      setLoading(true)
      await ticketService.seedDatabase()
      alert("Seeding completed successfully.")
      fetchTickets(1)
    } catch (err) {
      console.error("Seeding failed:", err)
      alert("Failed to seed database.")
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (newFilters) => {
    setFilters(newFilters)
    fetchTickets(1, newFilters)
  }

  const handlePageChange = (newPage) => {
    fetchTickets(newPage)
  }

  const handleViewTicket = async (ticketId) => {
    try {
      const ticket = await ticketService.getTicketById(ticketId)
      setSelectedTicket(ticket)
      setShowTicketModal(true)
    } catch (error) {
      console.error("Error fetching ticket:", error)
    }
  }

  const handleEditTicket = async (ticketId) => {
    try {
      const ticket = await ticketService.getTicketById(ticketId)
      setEditingTicket(ticket)
      setShowCreateModal(true)
    } catch (error) {
      console.error("Error fetching ticket:", error)
    }
  }

  const handleDeleteTicket = async (ticketId) => {
    if (window.confirm("Are you sure you want to delete this ticket?")) {
      try {
        await ticketService.deleteTicket(ticketId)
        fetchTickets(pagination.page)
      } catch (error) {
        console.error("Error deleting ticket:", error)
      }
    }
  }

  const handleCreateTicket = async (ticketData) => {
    try {
      if (editingTicket) {
        await ticketService.updateTicket(editingTicket.id, ticketData)
      } else {
        await ticketService.createTicket(ticketData)
      }
      setShowCreateModal(false)
      setEditingTicket(null)
      fetchTickets(pagination.page)
    } catch (error) {
      console.error("Error saving ticket:", error)
    }
  }

 


  return (
    <div className="bg-gray-50 flex h-screen">
      <div className="container mx-auto px-4 py-8 flex-1">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Support Ticketing System</h1>
          <p className="text-gray-600">Manage and track customer support tickets efficiently</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Tickets</h2>
              <div className="flex gap-2">
                <button
                  onClick={handleSeedDatabase}
                  className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg font-medium transition-colors"
                >
                  Seed Tickets
                </button>
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
                >
                  Create Ticket
                </button>
              </div>
            </div>

            <SearchFilters filters={filters} onSearch={handleSearch} loading={loading} />
          </div>

          <TicketTable
            tickets={tickets}
            loading={loading}
            pagination={pagination}
            onPageChange={handlePageChange}
            onViewTicket={handleViewTicket}
            onEditTicket={handleEditTicket}
            onDeleteTicket={handleDeleteTicket}
          />
        </div>

        {showTicketModal && (
          <TicketModal
            ticket={selectedTicket}
            onClose={() => {
              setShowTicketModal(false)
              setSelectedTicket(null)
            }}
          />
        )}

        {showCreateModal && (
          <CreateTicketModal
            ticket={editingTicket}
            onClose={() => {
              setShowCreateModal(false)
              setEditingTicket(null)
            }}
            onSave={handleCreateTicket}
          />
        )}

      </div>
    </div>
  )
}

export default App
