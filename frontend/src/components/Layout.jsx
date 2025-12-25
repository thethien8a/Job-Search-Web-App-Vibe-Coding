import { Outlet, Link } from 'react-router-dom'
import { Briefcase, Github } from 'lucide-react'

function Layout() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center gap-2 text-primary-600 hover:text-primary-700">
              <Briefcase className="w-8 h-8" />
              <span className="text-xl font-bold">JobSearch</span>
            </Link>
            <nav className="flex items-center gap-4">
              <a
                href="https://github.com/thethien8a/Job-Search-Web-App-Vibe-Coding"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-gray-900"
              >
                <Github className="w-5 h-5" />
              </a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-gray-500 text-sm">
            <p>© {new Date().getFullYear()} Dữ liệu được thu thập từ nhiều nguồn tuyển dụng.</p>
            <p className="mt-1">Vibe coded by Thế Thiện</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Layout
