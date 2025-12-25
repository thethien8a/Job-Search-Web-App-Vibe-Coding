import { MapPin, Building2, ExternalLink, Briefcase, Globe, User, Calendar } from 'lucide-react'

function JobCard({ job }) {
    return (
        <div className="card group">
            <div className="flex flex-col h-full">
                {/* Header */}
                <div className="flex justify-between items-start gap-4 mb-3">
                    <div className="flex-1 min-w-0">
                        <a
                            href={job.job_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-lg font-semibold text-gray-900 hover:text-primary-600 line-clamp-2 transition-colors"
                        >
                            {job.job_title}
                        </a>
                    </div>
                </div>

                {/* Company & Location & Position */}
                <div className="space-y-2 mb-4">
                    <div className="flex items-center gap-2 text-gray-600">
                        <Building2 className="w-4 h-4 shrink-0" />
                        <span className="truncate">{job.company_name}</span>
                    </div>
                    {job.location && (
                        <div className="flex items-center gap-2 text-gray-600">
                            <MapPin className="w-4 h-4 shrink-0" />
                            <span className="truncate">{job.location}</span>
                        </div>
                    )}
                    {job.job_position && (
                        <div className="flex items-center gap-2 text-gray-700 font-medium">
                            <User className="w-4 h-4 shrink-0" />
                            <span className="truncate">{job.job_position}</span>
                        </div>
                    )}
                </div>

                {/* Tags */}
                <div className="flex flex-wrap gap-2 mb-4">
                    {job.job_type && (
                        <span className="px-2 py-1 text-xs bg-blue-100 text-blue-600 rounded-full flex items-center gap-1">
                            <Briefcase className="w-3 h-3" />
                            {job.job_type}
                        </span>
                    )}
                    {job.work_arrangement && (
                        <span className="px-2 py-1 text-xs bg-green-100 text-green-600 rounded-full flex items-center gap-1">
                            <Globe className="w-3 h-3" />
                            {job.work_arrangement}
                        </span>
                    )}
                    {job.job_deadline && (
                        <span className="px-2 py-1 text-xs bg-orange-100 text-orange-600 rounded-full flex items-center gap-1">
                            <Calendar className="w-3 h-3" />
                            {job.job_deadline}
                        </span>
                    )}
                </div>

                {/* Footer - Only "Xem chi tiết" button that opens job_url */}
                <div className="mt-auto pt-4 border-t border-gray-100 flex justify-end">
                    <a
                        href={job.job_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center gap-1 hover:underline"
                    >
                        Xem chi tiết
                        <ExternalLink className="w-4 h-4" />
                    </a>
                </div>
            </div>
        </div>
    )
}

export default JobCard
