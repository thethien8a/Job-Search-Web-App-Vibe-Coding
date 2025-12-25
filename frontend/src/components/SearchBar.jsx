import { useState } from 'react'
import { Search, MapPin, Filter, X, Briefcase, Globe } from 'lucide-react'

function SearchBar({ onSearch, locations = [], jobTypes = [], workArrangements = [], initialFilters = {} }) {
  const [keyword, setKeyword] = useState(initialFilters.keyword || '')
  const [location, setLocation] = useState(initialFilters.location || '')
  const [jobType, setJobType] = useState(initialFilters.job_type || '')
  const [workArrangement, setWorkArrangement] = useState(initialFilters.work_arrangement || '')
  const [showFilters, setShowFilters] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    onSearch({
      keyword: keyword.trim() || undefined,
      location: location.trim() || undefined,
      job_type: jobType || undefined,
      work_arrangement: workArrangement || undefined,
    })
  }

  const handleClear = () => {
    setKeyword('')
    setLocation('')
    setJobType('')
    setWorkArrangement('')
    onSearch({})
  }

  const hasFilters = keyword || location || jobType || workArrangement

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="bg-white rounded-xl shadow-lg p-4 border border-gray-100 text-gray-900">
        {/* Main Search Row */}
        <div className="flex flex-col md:flex-row gap-3">
          {/* Keyword Input */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="Tìm kiếm việc làm, vị trí..."
              className="input-field pl-10"
            />
          </div>



          {/* Filter Toggle & Search Button */}
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => setShowFilters(!showFilters)}
              className={`btn-secondary flex items-center gap-2 ${showFilters ? 'bg-primary-100 text-primary-700' : ''}`}
            >
              <Filter className="w-4 h-4" />
              <span className="hidden sm:inline">Bộ lọc</span>
            </button>
            <button type="submit" className="btn-primary flex items-center gap-2">
              <Search className="w-4 h-4" />
              <span>Tìm kiếm</span>
            </button>
          </div>
        </div>

        {/* Expanded Filters */}
        {showFilters && (
          <div className="mt-4 pt-4 border-t border-gray-100">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Location Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Địa điểm
                </label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <select
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="input-field pl-10 appearance-none"
                  >
                    <option value="">Tất cả địa điểm</option>
                    {locations.map((loc) => (
                      <option key={loc} value={loc}>{loc}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Job Type Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Loại hình công việc
                </label>
                <div className="relative">
                  <Briefcase className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <select
                    value={jobType}
                    onChange={(e) => setJobType(e.target.value)}
                    className="input-field pl-10 appearance-none"
                  >
                    <option value="">Tất cả loại hình</option>
                    {jobTypes.map((type) => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Work Arrangement Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Hình thức làm việc
                </label>
                <div className="relative">
                  <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <select
                    value={workArrangement}
                    onChange={(e) => setWorkArrangement(e.target.value)}
                    className="input-field pl-10 appearance-none"
                  >
                    <option value="">Tất cả hình thức</option>
                    {workArrangements.map((arr) => (
                      <option key={arr} value={arr}>{arr}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Clear Filters */}
            {hasFilters && (
              <div className="mt-4 flex justify-end">
                <button
                  type="button"
                  onClick={handleClear}
                  className="text-sm text-gray-500 hover:text-gray-700 flex items-center gap-1"
                >
                  <X className="w-4 h-4" />
                  Xóa bộ lọc
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </form>
  )
}

export default SearchBar
