import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import {
  ArrowLeft,
  MapPin,
  Building2,
  Banknote,
  Star,
  ExternalLink,
  Calendar,
} from 'lucide-react'
import LoadingSpinner from '../components/LoadingSpinner'
import { getJobByUrl } from '../api/jobs'

function JobDetailPage() {
  const { id } = useParams()
  // Decode the URL parameter
  const jobUrl = decodeURIComponent(id)

  const { data: job, isLoading, isError, error } = useQuery({
    queryKey: ['job', jobUrl],
    queryFn: () => getJobByUrl(jobUrl),
  })

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <LoadingSpinner text="Đang tải thông tin việc làm..." />
      </div>
    )
  }

  if (isError) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="text-center">
          <div className="bg-red-50 text-red-600 p-6 rounded-xl inline-block">
            <p className="font-medium">Không thể tải thông tin việc làm</p>
            <p className="text-sm mt-1">{error.message}</p>
          </div>
          <Link to="/" className="mt-4 inline-flex items-center gap-2 text-primary-600 hover:text-primary-700">
            <ArrowLeft className="w-4 h-4" />
            Quay lại trang chủ
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-gray-50 min-h-screen py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Back Button */}
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Quay lại danh sách
        </Link>

        {/* Job Header */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
            {job.job_title}
          </h1>

          <div className="flex flex-wrap gap-4 text-gray-600">
            <div className="flex items-center gap-2">
              <Building2 className="w-5 h-5 text-gray-400" />
              <span className="font-medium">{job.company_name}</span>
            </div>
            {job.location && (
              <div className="flex items-center gap-2">
                <MapPin className="w-5 h-5 text-gray-400" />
                <span>{job.location}</span>
              </div>
            )}
          </div>

          {job.salary && (
            <div className="mt-4 flex items-center gap-2 text-green-600 font-semibold text-lg">
              <Banknote className="w-5 h-5" />
              <span>{job.salary}</span>
            </div>
          )}

          {/* Job Info Grid */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            {job.experience_level && (
              <div className="flex items-center gap-2 text-sm bg-blue-50 text-blue-700 p-3 rounded-lg">
                <Star className="w-4 h-4" />
                <span className="font-medium">Kinh nghiệm:</span>
                <span>{job.experience_level}</span>
              </div>
            )}
            {job.job_deadline && (
              <div className="flex items-center gap-2 text-sm bg-orange-50 text-orange-700 p-3 rounded-lg">
                <Calendar className="w-4 h-4" />
                <span className="font-medium">Hạn nộp:</span>
                <span>{job.job_deadline}</span>
              </div>
            )}
          </div>

          {/* Apply Button */}
          <div className="mt-6 flex flex-wrap gap-4">
            <a
              href={job.job_url}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary flex items-center gap-2"
            >
              <ExternalLink className="w-4 h-4" />
              Xem và ứng tuyển tại trang gốc
            </a>
          </div>
        </div>

        {/* Info Notice */}
        <div className="bg-blue-50 rounded-xl p-4 text-sm text-blue-700">
          <p className="flex items-center gap-2">
            <ExternalLink className="w-4 h-4" />
            Để xem đầy đủ mô tả công việc, yêu cầu và quyền lợi, vui lòng truy cập trang gốc của tin tuyển dụng.
          </p>
        </div>
      </div>
    </div>
  )
}

export default JobDetailPage
