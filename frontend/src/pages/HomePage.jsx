import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Briefcase, Building2, MapPin } from 'lucide-react'
import SearchBar from '../components/SearchBar'
import JobCard from '../components/JobCard'
import Pagination from '../components/Pagination'
import LoadingSpinner from '../components/LoadingSpinner'
import { searchJobs, getJobLocations, getJobTypes, getJobStats, getWorkArrangements } from '../api/jobs'

function HomePage() {
  const [filters, setFilters] = useState({})
  const [page, setPage] = useState(1)
  const pageSize = 12

  // Fetch locations for filter dropdown
  const { data: locations = [] } = useQuery({
    queryKey: ['locations'],
    queryFn: getJobLocations,
  })

  // Fetch job types for filter dropdown
  const { data: jobTypes = [] } = useQuery({
    queryKey: ['jobTypes'],
    queryFn: getJobTypes,
  })

  // Fetch work arrangements for filter dropdown
  const { data: workArrangements = [] } = useQuery({
    queryKey: ['workArrangements'],
    queryFn: getWorkArrangements,
  })

  // Fetch job statistics
  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: getJobStats,
  })

  // Fetch jobs with filters
  const { data: jobsData, isLoading, isError, error } = useQuery({
    queryKey: ['jobs', filters, page],
    queryFn: () => searchJobs({ ...filters, page, page_size: pageSize }),
  })

  const handleSearch = (newFilters) => {
    setFilters(newFilters)
    setPage(1) // Reset to first page on new search
  }

  const handlePageChange = (newPage) => {
    setPage(newPage)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 to-primary-800 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Tìm kiếm việc làm
            </h1>
            <p className="text-lg text-primary-100 max-w-2xl mx-auto">
              Khám phá hàng nghìn cơ hội việc làm từ nhiều nguồn tuyển dụng uy tín
            </p>
          </div>

          {/* Search Bar */}
          <div className="max-w-4xl mx-auto">
            <SearchBar
              onSearch={handleSearch}
              locations={locations}
              jobTypes={jobTypes}
              workArrangements={workArrangements}
              initialFilters={filters}
            />
          </div>

          {/* Stats */}
          {stats && (
            <div className="mt-8 flex flex-wrap justify-center gap-8">
              <div className="flex items-center gap-2 text-primary-100">
                <Briefcase className="w-5 h-5" />
                <span className="font-semibold text-white">{stats.total_jobs?.toLocaleString()}</span>
                <span>việc làm</span>
              </div>
              <div className="flex items-center gap-2 text-primary-100">
                <Building2 className="w-5 h-5" />
                <span className="font-semibold text-white">{stats.total_companies?.toLocaleString()}</span>
                <span>công ty</span>
              </div>
              <div className="flex items-center gap-2 text-primary-100">
                <MapPin className="w-5 h-5" />
                <span className="font-semibold text-white">{Object.keys(stats.jobs_by_location || {}).length}</span>
                <span>địa điểm</span>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Results Section */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Results Header */}
          {jobsData && (
            <div className="mb-6 flex justify-between items-center">
              <h2 className="text-xl font-semibold text-gray-900">
                Tìm thấy <span className="text-primary-600">{jobsData.total.toLocaleString()}</span> việc làm
              </h2>
              <span className="text-gray-500 text-sm">
                Trang {jobsData.page} / {jobsData.total_pages}
              </span>
            </div>
          )}

          {/* Loading State */}
          {isLoading && <LoadingSpinner text="Đang tìm kiếm việc làm..." />}

          {/* Error State */}
          {isError && (
            <div className="text-center py-12">
              <div className="bg-red-50 text-red-600 p-6 rounded-xl inline-block">
                <p className="font-medium">Đã xảy ra lỗi khi tải dữ liệu</p>
                <p className="text-sm mt-1">{error.message}</p>
              </div>
            </div>
          )}

          {/* Job Grid */}
          {jobsData && jobsData.items.length > 0 && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {jobsData.items.map((job) => (
                  <JobCard key={job.job_url} job={job} />
                ))}
              </div>

              {/* Pagination */}
              <div className="mt-8">
                <Pagination
                  currentPage={jobsData.page}
                  totalPages={jobsData.total_pages}
                  onPageChange={handlePageChange}
                />
              </div>
            </>
          )}

          {/* Empty State */}
          {jobsData && jobsData.items.length === 0 && (
            <div className="text-center py-12">
              <div className="bg-gray-50 p-8 rounded-xl inline-block">
                <Briefcase className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 font-medium">Không tìm thấy việc làm phù hợp</p>
                <p className="text-gray-500 text-sm mt-1">Thử thay đổi từ khóa hoặc bộ lọc</p>
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  )
}

export default HomePage
