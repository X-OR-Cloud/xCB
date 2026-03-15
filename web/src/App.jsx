import React, { useState, useEffect, useRef } from 'react';
import { 
  LayoutDashboard, 
  Database, 
  BookOpen, 
  Search, 
  Bell, 
  MoreVertical, 
  ChevronRight, 
  Users, 
  TrendingUp, 
  FileText, 
  Clock, 
  PlusSquare,
  Zap,
  Briefcase,
  AlertCircle,
  GraduationCap,
  ShieldCheck,
  Globe,
  Upload,
  RefreshCw,
  MoreHorizontal,
  Send,
  Link,
  Bot,
  User,
  Paperclip,
  Smile,
  Mic,
  Maximize2,
  Trash2,
  Settings,
  X,
  Folder,
  Activity
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// --- Shared Components ---

const SidebarLink = ({ icon: Icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center justify-between px-4 py-3 rounded-2xl transition-all duration-300 group ${
      active ? 'sidebar-item-active text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'
    }`}
  >
    <div className="flex items-center gap-3">
      <Icon size={20} className={active ? 'text-blue-500' : 'group-hover:text-white'} />
      <span className="text-sm font-medium">{label}</span>
    </div>
    {active && <div className="w-1 h-1 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.8)]" />}
  </button>
);

const AgentItem = ({ id, initials, name, desc, status, active, onClick }) => (
  <div 
    onClick={() => onClick(id)}
    className={`flex items-center justify-between px-4 py-2 rounded-2xl transition-all cursor-pointer group ${
      active ? 'bg-blue-600/10 border border-blue-500/20' : 'hover:bg-white/5'
    }`}
  >
    <div className="flex items-center gap-3">
      <div className={`w-9 h-9 rounded-xl flex items-center justify-center text-[10px] font-bold transition-all border ${
        active 
        ? 'bg-blue-600 border-blue-400 text-white' 
        : 'bg-slate-800 border-white/5 text-slate-400 group-hover:border-blue-500/30 group-hover:text-slate-200'
      }`}>
        {initials}
      </div>
      <div>
        <p className={`text-xs font-semibold transition-colors ${active ? 'text-white' : 'text-slate-300 group-hover:text-white'}`}>{name}</p>
        <p className="text-[10px] text-slate-500">{desc}</p>
      </div>
    </div>
    <div className={`w-1.5 h-1.5 rounded-full ${
      status === 'online' ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : 
      status === 'away' ? 'bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.6)]' : 'bg-slate-600'
    }`} />
  </div>
);

const StatCard = ({ icon: Icon, label, value, change, color }) => (
  <div className="glass-card p-6 flex-1 min-w-[240px]">
    <div className={`w-12 h-12 rounded-2xl bg-${color}-500/10 flex items-center justify-center mb-6`}>
      <Icon className={`text-${color}-500`} size={24} />
    </div>
    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">{label}</p>
    <h3 className="text-2xl font-black text-white mb-2">{value}</h3>
    <p className={`text-[10px] font-bold ${change.startsWith('+') ? 'text-blue-400' : 'text-red-400'}`}>
      {change} <span className="text-slate-500 font-normal">tháng này</span>
    </p>
  </div>
);

// --- Pages ---

const DashboardCEO = ({ stats, riskData }) => (
  <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
    <div className="flex flex-col gap-1">
      <h2 className="text-3xl font-black text-white tracking-tight">Tổng Quan Ban Lãnh Đạo</h2>
      <p className="text-slate-500 text-sm">Hiệu suất vận hành thời gian thực trên toàn hệ thống xHR HRAgent.</p>
    </div>

    {/* Top Row: KPIs */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[
        { label: "Tổng doanh thu (YTD)", value: stats.revenue_ytd || "---", change: stats.revenue_change, color: "blue", progress: 65 },
        { label: "Biên lợi nhuận ròng", value: stats.margin || "---", change: stats.margin_change, color: "blue", progress: 45 },
        { label: "Chỉ số rủi ro", value: stats.risk_index || "---", change: stats.risk_change, color: "purple", progress: 15 },
        { label: "Mức độ hoàn thành mục tiêu", value: stats.goal_completion || "---", change: stats.goal_change, color: "emerald", progress: 88 }
      ].map((kpi, i) => (
        <div key={i} className="glass-card p-6 border-white/[0.03]">
          <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-4">{kpi.label}</p>
          <div className="flex items-baseline gap-2 mb-4">
            <h3 className="text-2xl font-black text-white">{kpi.value}</h3>
            <span className={`text-[10px] font-bold ${kpi.change?.startsWith('+') ? 'text-green-500' : 'text-slate-500'}`}>{kpi.change}</span>
          </div>
          <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
             <div className={`h-full rounded-full ${
               kpi.color === 'blue' ? 'bg-blue-500' : 
               kpi.color === 'purple' ? 'bg-purple-500' : 'bg-green-500'
             }`} style={{ width: `${kpi.progress}%` }} />
          </div>
        </div>
      ))}
    </div>

    {/* Middle Row: Map & Alerts */}
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
      {/* Global Map */}
      <div className="lg:col-span-8 glass-card p-8 bg-white/[0.01]">
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-lg font-bold text-white">Phân bổ nguồn nhân lực toàn cầu</h3>
          <div className="flex items-center gap-6">
             <div className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                <span className="text-[10px] font-bold text-slate-500 uppercase">Tăng trưởng cao</span>
             </div>
             <div className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-purple-500" />
                <span className="text-[10px] font-bold text-slate-500 uppercase">Ổn định</span>
             </div>
          </div>
        </div>
        <div className="h-[400px] w-full bg-slate-900/40 rounded-3xl relative overflow-hidden border border-white/5">
           {/* Abstract Map Dots */}
           <motion.div animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0.8, 0.5] }} transition={{ duration: 4, repeat: Infinity }} className="absolute top-1/3 left-1/4 w-3 h-3 bg-blue-500 rounded-full blur-[2px]" />
           <motion.div animate={{ scale: [1, 1.3, 1], opacity: [0.4, 0.7, 0.4] }} transition={{ duration: 5, repeat: Infinity, delay: 1 }} className="absolute top-1/2 left-1/2 w-3 h-3 bg-blue-400 rounded-full blur-[2px]" />
           <motion.div animate={{ scale: [1, 1.2, 1], opacity: [0.6, 0.9, 0.6] }} transition={{ duration: 3, repeat: Infinity, delay: 2 }} className="absolute top-2/3 left-[40%] w-3 h-3 bg-purple-500 rounded-full blur-[2px]" />
           <motion.div animate={{ scale: [1, 1.4, 1], opacity: [0.5, 0.8, 0.5] }} transition={{ duration: 6, repeat: Infinity, delay: 0.5 }} className="absolute bottom-1/4 right-1/4 w-3 h-3 bg-blue-600 rounded-full blur-[2px]" />
           <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/20" />
        </div>
      </div>

      {/* Strategic Alerts & AI Insights */}
      <div className="lg:col-span-4 space-y-8">
        {/* Alerts */}
        <div className="glass-card p-6 bg-white/[0.01]">
           <h3 className="text-sm font-bold text-white mb-6 flex items-center gap-2">
             <AlertCircle size={18} className="text-blue-500" />
             Cảnh báo chiến lược
           </h3>
           <div className="space-y-4">
              <div className="bg-red-500/5 border border-red-500/10 rounded-2xl p-4">
                 <p className="text-[9px] font-black text-red-500 uppercase tracking-widest mb-1">RỦI RO NGHIÊM TRỌNG</p>
                 <p className="text-xs text-slate-400 leading-relaxed">Phát hiện gián đoạn chuỗi cung ứng tại khu vực APAC. Dự kiến ảnh hưởng 12%.</p>
              </div>
              <div className="bg-blue-600/5 border border-blue-500/10 rounded-2xl p-4">
                 <p className="text-[9px] font-black text-blue-500 uppercase tracking-widest mb-1">CƠ HỘI</p>
                 <p className="text-xs text-slate-400 leading-relaxed">Tín hiệu thâm nhập thị trường mới tại EU cho lĩnh vực năng lượng tái tạo.</p>
              </div>
           </div>
        </div>

        {/* AI Insights */}
        <div className="glass-card p-6 bg-white/[0.01]">
           <h3 className="text-sm font-bold text-white mb-6 flex items-center gap-2">
             <Zap size={18} className="text-purple-500" />
             Thông tin chi tiết từ AI
           </h3>
           <div className="space-y-6">
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center shrink-0 border border-purple-500/20">
                  <TrendingUp size={18} className="text-purple-500" />
                </div>
                <div>
                  <p className="text-xs font-bold text-white mb-1">Phân tích xu hướng</p>
                  <p className="text-[10px] text-slate-500 leading-relaxed">Tăng trưởng doanh thu đang vượt mức chi tiêu 2.4 lần trong quý này.</p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center shrink-0 border border-blue-500/20">
                  <Activity size={18} className="text-blue-500" />
                </div>
                <div>
                  <p className="text-xs font-bold text-white mb-1">Dự báo</p>
                  <p className="text-[10px] text-slate-500 leading-relaxed">Dự kiến mức hoàn thành mục tiêu: 94% vào cuối quý 4.</p>
                </div>
              </div>
           </div>
        </div>
      </div>
    </div>

    {/* Bottom Row: Chart & Risk */}
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <div className="lg:col-span-7 glass-card p-8">
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-lg font-bold text-white">Xu hướng tăng trưởng doanh thu</h3>
          <select className="bg-white/5 border border-white/10 rounded-xl px-3 py-1.5 text-[10px] font-bold text-slate-400 outline-none">
            <option>6 tháng qua</option>
          </select>
        </div>
        <div className="h-48 flex items-end gap-4 px-2">
           {[
             { m: 'T10', v: 45, val: '$12.5M' },
             { m: 'T11', v: 52, val: '$14.2M' },
             { m: 'T12', v: 48, val: '$13.1M' },
             { m: 'T1', v: 65, val: '$18.4M' },
             { m: 'T2', v: 78, val: '$21.5M' },
             { m: 'T3', v: 92, val: '$25.8M' }
           ].map((data, i) => (
             <div key={i} className="flex-1 flex flex-col items-center gap-3 group h-full">
                <div className="w-full bg-blue-600/10 rounded-t-xl relative flex items-end justify-center overflow-hidden h-full">
                   <motion.div 
                    initial={{ height: 0 }}
                    animate={{ height: `${data.v}%` }}
                    className="w-full bg-gradient-to-t from-blue-600 to-blue-400 rounded-t-xl group-hover:brightness-125 transition-all shadow-[0_0_15px_rgba(59,130,246,0.3)]"
                   />
                   <div className="absolute top-2 opacity-0 group-hover:opacity-100 transition-all transform -translate-y-2 group-hover:translate-y-0 text-[10px] font-black text-white bg-blue-600 px-2 py-1 rounded-lg shadow-xl z-10">
                    {data.val}
                   </div>
                </div>
                <span className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">{data.m}</span>
             </div>
           ))}
        </div>
      </div>

      <div className="lg:col-span-5 glass-card p-8">
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-lg font-bold text-white">Phân tích rủi ro theo phòng ban</h3>
          <span className="px-3 py-1 rounded-lg bg-green-500/10 text-[9px] font-black text-green-500 uppercase tracking-widest border border-green-500/20">ỔN ĐỊNH</span>
        </div>
        <div className="space-y-6">
           {riskData.map((item, i) => (
             <div key={i} className="space-y-2">
                <div className="flex justify-between text-[10px] font-bold text-slate-500 uppercase">
                   <span>{item.dept}</span>
                   <span className="text-white">{item.risk}%</span>
                </div>
                <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-600 rounded-full" style={{ width: `${item.risk}%` }} />
                </div>
             </div>
           ))}
        </div>
      </div>
    </div>
  </motion.div>
);

const DataManager = ({ onUpload }) => {
  const fileInputRef = useRef(null);
  
  // Mock data for storage and monthly usage
  const storageStats = {
    total: 12.5, // TB
    used: 4.8,   // TB
    percentage: 38.4,
    monthlyUsage: [0.8, 1.2, 0.9, 1.5, 2.1, 1.8], // TB per month for last 6 months
    months: ['T10', 'T11', 'T12', 'T1', 'T2', 'T3']
  };

  // Mock data for processing queue
  const mockFiles = [
    { ten_file: "HOP_DONG_LD_2024_V1.pdf", dung_luong: 4500, tien_do_ocr: 100, tien_do_vector: 85, status: 'processing' },
    { ten_file: "BANG_DIEM_K25_MARCH.xlsx", dung_luong: 2100, tien_do_ocr: 100, tien_do_vector: 100, status: 'completed' },
    { ten_file: "SCAN_HOSO_THUYENVIEN_001.jpg", dung_luong: 12000, tien_do_ocr: 45, tien_do_vector: 0, status: 'ocr_scanning' },
    { ten_file: "CHINH_SACH_BAOHIEM_NHATBAN.pdf", dung_luong: 8500, tien_do_ocr: 0, tien_do_vector: 0, status: 'queued' }
  ];

  const handleFileChange = (e) => {
    if (e.target.files?.[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-10">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-1">
          <h2 className="text-3xl font-bold text-white tracking-tight">Trung tâm Nạp dữ liệu</h2>
          <p className="text-slate-500 text-sm">Quản lý nạp tri thức và quy trình xử lý tài liệu</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-blue-500/5 border border-blue-500/10 px-4 py-2 rounded-full">
            <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
            <span className="text-[10px] font-bold text-blue-500 uppercase tracking-widest">Hệ thống đang Sẵn sàng</span>
          </div>
        </div>
      </div>

      {/* Storage Report Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="glass-card p-8 bg-blue-500/[0.02]">
          <div className="flex items-center gap-4 mb-8">
             <div className="w-10 h-10 rounded-xl bg-blue-600/10 flex items-center justify-center border border-blue-500/20">
               <Database size={20} className="text-blue-500" />
             </div>
             <h3 className="text-sm font-bold text-white uppercase tracking-widest">Dung lượng Lưu trữ</h3>
          </div>
          <div className="flex items-baseline gap-2 mb-2">
            <h4 className="text-4xl font-black text-white">{storageStats.used}</h4>
            <span className="text-lg font-bold text-slate-500">/ {storageStats.total} TB</span>
          </div>
          <div className="flex justify-between items-center mb-4 text-[10px] font-bold">
             <span className="text-blue-400">ĐÃ SỬ DỤNG {storageStats.percentage}%</span>
             <span className="text-slate-600">{storageStats.total - storageStats.used} TB CÒN TRỐNG</span>
          </div>
          <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
            <div className="h-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)] transition-all duration-1000" style={{ width: `${storageStats.percentage}%` }} />
          </div>
        </div>

        <div className="lg:col-span-2 glass-card p-8 bg-white/[0.01]">
          <div className="flex items-center justify-between mb-8">
             <div className="flex items-center gap-4">
               <div className="w-10 h-10 rounded-xl bg-purple-600/10 flex items-center justify-center border border-purple-500/20">
                 <TrendingUp size={20} className="text-purple-500" />
               </div>
               <h3 className="text-sm font-bold text-white uppercase tracking-widest">Tình hình sử dụng trong tháng (TB)</h3>
             </div>
             <div className="px-3 py-1 bg-white/5 rounded-lg text-slate-500 text-[10px] font-bold">+24% so với năm ngoái</div>
          </div>
          <div className="h-24 flex items-end gap-4">
            {storageStats.monthlyUsage.map((val, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-2 group">
                <div className="w-full bg-blue-600/10 rounded-t-lg relative flex items-end justify-center overflow-hidden">
                   <motion.div 
                    initial={{ height: 0 }}
                    animate={{ height: `${(val / 2.5) * 100}%` }}
                    className="w-full bg-gradient-to-t from-blue-600 to-blue-400 rounded-t-lg group-hover:brightness-125 transition-all"
                   />
                   <div className="absolute top-2 opacity-0 group-hover:opacity-100 transition-opacity text-[9px] font-bold text-white bg-black/50 px-1 rounded">{val}T</div>
                </div>
                <span className="text-[9px] font-bold text-slate-600 uppercase">{storageStats.months[i]}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Local Folder Sync */}
        <div className="glass-card p-8 group relative overflow-hidden">
          <div className="flex justify-between items-start mb-8">
            <div>
              <h3 className="text-xl font-bold text-white mb-2">Đồng bộ Thư mục Cục bộ</h3>
              <p className="text-slate-500 text-xs max-w-xs leading-relaxed">
                Tự động giám sát và nạp tệp từ cơ sở hạ tầng lưu trữ nội bộ của bạn.
              </p>
            </div>
            <button className="w-12 h-12 rounded-2xl bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-500 hover:bg-blue-600 hover:text-white transition-all">
              <RefreshCw size={20} />
            </button>
          </div>

          <div className="bg-black/40 border border-white/5 rounded-2xl p-6 flex items-center justify-between mb-8 group-hover:border-blue-500/20 transition-all">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center">
                <Folder size={24} className="text-slate-400" />
              </div>
              <div>
                <p className="text-[10px] font-bold text-slate-600 uppercase tracking-widest mb-1">Đường dẫn đồng bộ hiện tại</p>
                <p className="text-sm font-bold text-blue-500 font-mono">C:/Users/HR/Documents/Scanning</p>
              </div>
            </div>
            <button className="px-4 py-2 text-[10px] font-black text-slate-400 border border-white/10 rounded-xl hover:bg-white/5 transition-all">
              THAY ĐỔI
            </button>
          </div>
        </div>

        {/* Manual Upload */}
        <div 
          onClick={() => fileInputRef.current?.click()}
          className="glass-card p-10 border-dashed border-2 border-white/5 flex flex-col items-center justify-center text-center group hover:border-blue-500/30 transition-all cursor-pointer"
        >
          <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" />
          <div className="w-20 h-20 rounded-[2.5rem] bg-slate-800 border border-white/5 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-500">
            <Upload className="text-white" size={32} />
          </div>
          <h3 className="text-2xl font-bold text-white mb-2">Tải lên Thủ công</h3>
          <p className="text-slate-500 text-sm max-w-xs mb-8">
            Kéo và thả tài liệu vào đây hoặc <span className="text-blue-500 font-bold">duyệt tệp</span>. Hỗ trợ PDF, Word, và Hình ảnh.
          </p>
        </div>
      </div>

      {/* Processing Queue */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-white">Hàng đợi Xử lý (Mockdata)</h3>
          <span className="px-3 py-1 bg-white/5 rounded-lg text-[10px] font-bold text-slate-500 uppercase tracking-widest">Đang xử lý: 3</span>
        </div>

        <div className="space-y-4">
          {mockFiles.map((file, i) => (
            <div key={i} className="glass-card p-6 flex items-center gap-8 group hover:bg-white/[0.02] transition-all">
              <div className="w-12 h-12 rounded-xl flex items-center justify-center border border-white/5 bg-blue-600/10">
                <FileText size={20} className="text-slate-400" />
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-sm font-bold text-white truncate">{file.ten_file}</h4>
                  <span className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">{Math.round(file.dung_luong / 1024)} MB</span>
                </div>
                
                <div className="grid grid-cols-2 gap-8">
                  <div>
                    <div className="flex justify-between items-center mb-1.5">
                      <span className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">OCR</span>
                      <span className={`text-[9px] font-bold ${file.tien_do_ocr === 100 ? 'text-green-500' : 'text-blue-400'}`}>
                        {file.tien_do_ocr}%
                      </span>
                    </div>
                    <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-blue-500" style={{ width: `${file.tien_do_ocr}%` }} />
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between items-center mb-1.5">
                      <span className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">VECTOR</span>
                      <span className={`text-[9px] font-bold ${file.tien_do_vector === 100 ? 'text-purple-500' : 'text-purple-400'}`}>
                        {file.tien_do_vector}%
                      </span>
                    </div>
                    <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-purple-500" style={{ width: `${file.tien_do_vector}%` }} />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};

const KnowledgeBase = () => {
  const [searchQuery, setSearchQuery] = useState('');
  
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-10">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-1">
          <h2 className="text-4xl font-black text-white tracking-tight">Cơ sở Tri thức</h2>
          <p className="text-slate-500 text-sm">Quản lý bộ sưu tập vector và chỉ mục tìm kiếm ngữ nghĩa</p>
        </div>
        <button className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-2xl text-xs font-black shadow-lg shadow-blue-600/30 hover:bg-blue-500 transition-all active:scale-95">
          <PlusSquare size={18} />
          TẠO BỘ SƯU TẬP
        </button>
      </div>

      {/* Top Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-8 group">
          <p className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] mb-4">TỔNG SỐ TÀI LIỆU</p>
          <div className="flex items-baseline gap-3">
            <h3 className="text-3xl font-black text-white">4,280</h3>
            <span className="text-xs font-bold text-green-500">+12%</span>
          </div>
        </div>
        <div className="glass-card p-8 group">
          <p className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] mb-4">VECTOR EMBEDDINGS</p>
          <div className="flex items-baseline gap-3">
            <h3 className="text-3xl font-black text-white">1.2M</h3>
            <span className="text-[10px] font-bold text-green-500 uppercase">Đã tối ưu</span>
          </div>
        </div>
        <div className="glass-card p-8 group">
          <p className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] mb-4">CHỈ MỤC RAG HOẠT ĐỘNG</p>
          <div className="flex items-baseline gap-3">
            <h3 className="text-3xl font-black text-white">12</h3>
            <span className="text-[10px] font-bold text-blue-500 uppercase">3 Đang chạy</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: Collections */}
        <div className="lg:col-span-8 space-y-8">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold text-white">Bộ sưu tập Tri thức</h3>
            <div className="flex gap-2">
              <button className="p-2 rounded-lg bg-blue-600/20 text-blue-500 border border-blue-500/20"><LayoutDashboard size={18} /></button>
              <button className="p-2 rounded-lg hover:bg-white/5 text-slate-600"><MoreVertical size={18} className="rotate-90" /></button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Card 1 */}
            <div className="glass-card p-8 group cursor-pointer hover:border-blue-500/30 transition-all">
              <div className="flex justify-between items-start mb-8">
                <div className="flex gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
                    <Globe className="text-blue-500" size={24} />
                  </div>
                  <div>
                    <h4 className="text-lg font-bold text-white">Thị trường Nhật Bản</h4>
                    <p className="text-[10px] text-slate-600 font-mono">nhat_ban</p>
                  </div>
                </div>
                <span className="px-3 py-1 rounded-lg bg-blue-500/10 text-[9px] font-black text-blue-500 uppercase tracking-widest border border-blue-500/20">MẬT ĐỘ CAO</span>
              </div>
              <div className="flex gap-10 mb-8">
                <div>
                  <p className="text-[9px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-1">TÀI LIỆU</p>
                  <p className="text-lg font-black text-slate-300">1,200</p>
                </div>
                <div>
                  <p className="text-[9px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-1">CẬP NHẬT</p>
                  <p className="text-lg font-black text-slate-300">5p trước</p>
                </div>
              </div>
              <div className="space-y-3">
                <p className="text-[9px] font-black text-blue-500/60 uppercase tracking-widest">SỨC KHỎE VECTOR</p>
                <div className="h-10 w-full bg-blue-500/5 rounded-xl overflow-hidden relative">
                   {/* Simple SVG wave representing health */}
                   <svg className="absolute bottom-0 left-0 w-full h-8 text-blue-500/40" preserveAspectRatio="none" viewBox="0 0 400 100">
                     <path d="M0,50 C50,20 100,80 150,50 C200,20 250,80 300,50 C350,20 400,80 400,50 V100 H0 Z" fill="currentColor" />
                     <path d="M0,60 C50,30 100,90 150,60 C200,30 250,90 300,60 C400,30 400,90 400,60 V100 H0 Z" fill="rgba(59,130,246,0.2)" />
                   </svg>
                </div>
              </div>
            </div>

            {/* Card 2 */}
            <div className="glass-card p-8 group cursor-pointer hover:border-purple-500/30 transition-all">
              <div className="flex justify-between items-start mb-8">
                <div className="flex gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-purple-500/10 flex items-center justify-center border border-purple-500/20">
                    <Database className="text-purple-500" size={24} />
                  </div>
                  <div>
                    <h4 className="text-lg font-bold text-white">Quản lý Thuyền viên</h4>
                    <p className="text-[10px] text-slate-600 font-mono">thuy_en_vien</p>
                  </div>
                </div>
                <span className="px-3 py-1 rounded-lg bg-green-500/10 text-[9px] font-black text-green-500 uppercase tracking-widest border border-green-500/20 text-center leading-tight">RAG HOẠT ĐỘNG</span>
              </div>
              <div className="flex gap-10 mb-8">
                <div>
                  <p className="text-[9px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-1">TÀI LIỆU</p>
                  <p className="text-lg font-black text-slate-300">850</p>
                </div>
                <div>
                  <p className="text-[9px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-1">CẬP NHẬT</p>
                  <p className="text-lg font-black text-slate-300">1g trước</p>
                </div>
              </div>
              <div className="space-y-3">
                <p className="text-[9px] font-black text-purple-500/60 uppercase tracking-widest">SỨC KHỎE VECTOR</p>
                <div className="h-10 w-full bg-purple-500/5 rounded-xl overflow-hidden relative">
                   <svg className="absolute bottom-0 left-0 w-full h-8 text-purple-500/40" preserveAspectRatio="none" viewBox="0 0 400 100">
                     <path d="M0,80 C100,20 200,90 300,40 C400,80 400,0 400,0 V100 H0 Z" fill="currentColor" />
                   </svg>
                </div>
              </div>
            </div>

            {/* Card 3 */}
            <div className="glass-card p-8 group cursor-pointer hover:border-amber-500/30 transition-all">
              <div className="flex justify-between items-start mb-8">
                <div className="flex gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-amber-500/10 flex items-center justify-center border border-amber-500/20">
                    <GraduationCap className="text-amber-500" size={24} />
                  </div>
                  <div>
                    <h4 className="text-lg font-bold text-white">Trung tâm Đào tạo</h4>
                    <p className="text-[10px] text-slate-600 font-mono">dao_tao</p>
                  </div>
                </div>
                <span className="px-3 py-1 rounded-lg bg-amber-500/10 text-[9px] font-black text-amber-500 uppercase tracking-widest border border-amber-500/20 italic">ĐANG XỬ LÝ</span>
              </div>
              <div className="flex gap-10 mb-8">
                <div>
                  <p className="text-[9px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-1">TÀI LIỆU</p>
                  <p className="text-lg font-black text-slate-300">430</p>
                </div>
                <div>
                  <p className="text-[9px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-1">CẬP NHẬT</p>
                  <p className="text-lg font-black text-slate-300">20p trước</p>
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center text-[9px] font-black text-slate-600 transition-all group-hover:text-amber-500/60 transition-all uppercase tracking-widest">
                  <span>TIẾN TRÌNH EMBEDDING 65%</span>
                </div>
                <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full w-[65%] bg-blue-600 rounded-full shadow-[0_0_8px_rgba(37,99,235,0.4)]" />
                </div>
              </div>
            </div>

            {/* Card 4 */}
            <div className="glass-card p-8 group cursor-pointer hover:border-blue-500/30 transition-all">
              <div className="flex justify-between items-start mb-8">
                <div className="flex gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
                    <Briefcase className="text-blue-500" size={24} />
                  </div>
                  <div>
                    <h4 className="text-lg font-bold text-white">Hành chính - Kế toán</h4>
                    <p className="text-[10px] text-slate-600 font-mono">hanh_chinh</p>
                  </div>
                </div>
                <span className="px-3 py-1 rounded-lg bg-blue-500/10 text-[9px] font-black text-blue-500 uppercase tracking-widest border border-blue-500/20">MẬT ĐỘ CAO</span>
              </div>
              <div className="flex gap-10 mb-8">
                <div>
                  <p className="text-[9px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-1">TÀI LIỆU</p>
                  <p className="text-lg font-black text-slate-300">1.8k</p>
                </div>
                <div>
                  <p className="text-[9px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-1">CẬP NHẬT</p>
                  <p className="text-lg font-black text-slate-300">Hôm qua</p>
                </div>
              </div>
              <div className="space-y-3">
                <p className="text-[9px] font-black text-blue-500/60 uppercase tracking-widest">SỨC KHỎE VECTOR</p>
                <div className="h-10 w-full bg-blue-500/5 rounded-xl overflow-hidden relative">
                   <svg className="absolute bottom-0 left-0 w-full h-8 text-blue-500/40" preserveAspectRatio="none" viewBox="0 0 400 100">
                     <path d="M0,80 C50,90 100,70 150,85 C200,95 250,75 300,88 C350,95 400,75 400,85 V100 H0 Z" fill="currentColor" />
                   </svg>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Semantic Search Preview */}
        <div className="lg:col-span-4 space-y-6">
          <div className="glass-card p-8 bg-blue-500/[0.02] border-blue-500/10">
            <h3 className="text-lg font-bold text-white flex items-center gap-3 mb-8">
              <Zap className="text-blue-500" size={20} />
              Xem trước Tìm kiếm Ngữ nghĩa
            </h3>

            <div className="relative mb-8">
              <textarea 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Nhập truy vấn để kiểm tra cơ sở tri thức..."
                className="w-full h-32 bg-black/40 border border-white/5 rounded-2xl p-6 text-sm text-slate-300 placeholder:text-slate-700 outline-none focus:border-blue-500/30 transition-all resize-none"
              />
              <button className="absolute bottom-4 right-4 p-3 bg-blue-600 text-white rounded-xl shadow-lg shadow-blue-600/20 hover:bg-blue-500 transition-all">
                <Send size={18} />
              </button>
            </div>

            <div className="space-y-6">
              <div>
                <p className="text-[9px] font-black text-slate-600 uppercase tracking-[0.2em] mb-4">TRUY VẤN VÍ DỤ</p>
                <div className="p-4 bg-white/[0.02] border border-white/5 rounded-2xl cursor-pointer hover:bg-white/5 transition-all">
                  <p className="text-xs text-slate-400 italic">"Các yêu cầu về visa đối với thị trường Nhật Bản là gì?"</p>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-4">
                  <p className="text-[9px] font-black text-slate-600 uppercase tracking-[0.2em]">KẾT QUẢ</p>
                  <span className="text-[9px] font-bold text-blue-500 uppercase tracking-widest">Trùng khớp Nhất (98%)</span>
                </div>
                <div className="p-6 bg-blue-600/5 border border-blue-500/10 rounded-2xl space-y-3">
                  <div className="flex items-center gap-2 text-blue-400">
                    <FileText size={14} />
                    <span className="text-[10px] font-bold uppercase tracking-widest">CHINH_SACH_VISA_V4.PDF</span>
                  </div>
                  <p className="text-[11px] leading-relaxed text-slate-400">
                    "Tất cả các thuyền viên được chỉ định cho các tàu thuộc Thị trường Nhật Bản phải sở hữu Số thuyền viên hợp lệ và Visa lao động do Lãnh sự quán cấp..."
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

const AgentChat = ({ agent, onSendMessage }) => {
  const [messages, setMessages] = useState([
    { id: 1, text: `Chào quản trị viên, tôi là ${agent.name}. Bạn cần hỗ trợ gì về ${agent.desc} hôm nay?`, sender: 'bot', time: '10:00' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim()) return;
    const userMsg = { id: Date.now(), text: inputValue, sender: 'user', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    setMessages([...messages, userMsg]);
    setInputValue('');
    
    try {
      const reply = await onSendMessage(agent.id, inputValue);
      const botMsg = {
        id: Date.now() + 1,
        text: reply,
        sender: 'bot',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setMessages(prev => [...prev, { id: Date.now()+1, text: "Lỗi kết nối BOT. Hãy thử lại.", sender: 'bot', color: 'red' }]);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.98 }} 
      animate={{ opacity: 1, scale: 1 }} 
      className="h-full flex flex-col glass-card bg-[#0d0f16]/80 p-0 overflow-hidden"
    >
      {/* Chat Header */}
      <header className="px-8 py-5 border-b border-white/5 flex items-center justify-between bg-black/20">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-blue-600 border border-blue-400 flex items-center justify-center text-sm font-bold text-white shadow-lg">
            {agent.initials}
          </div>
          <div>
            <h3 className="font-bold text-white text-lg">{agent.name}</h3>
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Đang phản hồi</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button className="p-2.5 rounded-xl hover:bg-white/5 text-slate-500 transition-all"><Settings size={18} /></button>
          <button className="p-2.5 rounded-xl hover:bg-white/5 text-slate-500 transition-all"><Maximize2 size={18} /></button>
          <button className="p-2.5 rounded-xl hover:bg-red-500/10 text-slate-500 hover:text-red-400 transition-all"><Trash2 size={18} /></button>
        </div>
      </header>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-8 space-y-6 custom-scrollbar">
        {messages.map((m) => (
          <div key={m.id} className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex gap-4 max-w-[70%] ${m.sender === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-lg shrink-0 flex items-center justify-center ${
                m.sender === 'user' ? 'bg-blue-600' : 'bg-slate-800 border border-white/5'
              }`}>
                {m.sender === 'user' ? <User size={14} className="text-white" /> : <Bot size={14} className="text-blue-500" />}
              </div>
              <div className="space-y-2">
                <div className={`p-4 rounded-2xl text-sm leading-relaxed ${
                  m.sender === 'user' 
                  ? 'bg-blue-600 text-white rounded-tr-none shadow-lg' 
                  : 'bg-white/[0.03] text-slate-300 border border-white/5 rounded-tl-none'
                }`}>
                  {m.text}
                </div>
                <p className={`text-[10px] font-bold text-slate-600 ${m.sender === 'user' ? 'text-right' : 'text-left'}`}>
                  {m.time}
                </p>
              </div>
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-8 border-t border-white/5 bg-black/40">
        <div className="relative glass-card bg-white/[0.04] p-2 flex items-center gap-2 border-white/10 focus-within:border-blue-500/50 transition-all">
          <button className="p-2 rounded-xl hover:bg-white/5 text-slate-500 transition-all">
            <Paperclip size={18} />
          </button>
          <input 
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            type="text" 
            placeholder={`Hỏi ${agent.name} về dữ liệu ${agent.desc}...`}
            className="flex-1 bg-transparent border-none outline-none text-sm py-2 px-2 text-white placeholder-slate-600"
          />
          <div className="flex items-center gap-1 border-l border-white/5 pl-2">
            <button className="p-2 rounded-xl hover:bg-white/5 text-slate-500 transition-all">
              <Smile size={18} />
            </button>
            <button className="p-2 rounded-xl hover:bg-white/5 text-slate-500 transition-all">
              <Mic size={18} />
            </button>
            <button 
              onClick={handleSend}
              className="p-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl shadow-lg shadow-blue-600/20 active:scale-95 transition-all ml-2"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// --- Layout & Main App ---

const API_BASE = 'http://localhost:8000/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [activeAgentId, setActiveAgentId] = useState(null);
  const [dashboardStats, setDashboardStats] = useState({});
  const [riskData, setRiskData] = useState([]);
  const [files, setFiles] = useState([]);
  const [collections, setCollections] = useState([]);

  // Fetch initial data
  useEffect(() => {
    fetchStats();
    fetchFiles();
    fetchCollections();
    const interval = setInterval(() => {
      fetchFiles(); // Refresh processing status every 5s
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/dashboard/stats`);
      const data = await res.json();
      setDashboardStats(data);
      const resRisk = await fetch(`${API_BASE}/dashboard/risk-analysis`);
      setRiskData(await resRisk.json());
    } catch (e) { console.error("Fetch stats error", e); }
  };

  const fetchFiles = async () => {
    try {
      const res = await fetch(`${API_BASE}/data/files`);
      setFiles(await res.json());
    } catch (e) { console.error("Fetch files error", e); }
  };

  const fetchCollections = async () => {
    try {
      const res = await fetch(`${API_BASE}/kb/collections`);
      setCollections(await res.json());
    } catch (e) { console.error("Fetch collections error", e); }
  };

  const handleUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('phong_ban', 'hanh_chinh');
    try {
      await fetch(`${API_BASE}/data/upload`, { method: 'POST', body: formData });
      fetchFiles();
    } catch (e) { console.error("Upload error", e); }
  };

  const handleSendMessage = async (agentId, message) => {
    const res = await fetch(`${API_BASE}/chat/${agentId}?message=${encodeURIComponent(message)}`, {
      method: 'POST'
    });
    const data = await res.json();
    return data.reply;
  };

  const agents = [
    { id: 'nb', initials: 'NB', name: 'MOLTY-NB', desc: 'Thị trường Nhật Bản', status: 'online' },
    { id: 'tv', initials: 'TV', name: 'MOLTY-TV', desc: 'Quản lý Thuyền viên', status: 'online' },
    { id: 'hc', initials: 'HC', name: 'MOLTY-HC', desc: 'Hành chính & HR', status: 'away' },
    { id: 'ceo', initials: 'AI', name: 'MOLTY-CEO', desc: 'Điều hành Hệ thống', status: 'online' },
  ];

  const handleAgentClick = (id) => {
    setActiveAgentId(id);
    setActiveTab('chat');
  };

  const renderContent = () => {
    if (activeTab === 'chat' && activeAgentId) {
      const agent = agents.find(a => a.id === activeAgentId);
      return <AgentChat agent={agent} onSendMessage={handleSendMessage} />;
    }

    switch(activeTab) {
      case 'dashboard': return <DashboardCEO stats={dashboardStats} riskData={riskData} />;
      case 'data': return <DataManager onUpload={handleUpload} />;
      case 'kb': return <KnowledgeBase collections={collections} />;
      default: return <DashboardCEO stats={dashboardStats} riskData={riskData} />;
    }
  };

  return (
    <div className="flex h-screen bg-[#0a0c10] text-[#e2e8f0] font-sans selection:bg-blue-500/30 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-72 bg-[#0c0e14] border-r border-white/5 flex flex-col shrink-0">
        <div className="p-10 flex items-center gap-4">
          <div className="w-12 h-12 flex items-center justify-center">
            <img src="/logo.png" alt="xHR Logo" className="w-full h-full object-contain" />
          </div>
          <div className="leading-tight">
            <h1 className="font-black text-2xl tracking-tighter text-white">xHR</h1>
            <p className="text-[9px] font-bold text-slate-600 tracking-widest uppercase">AI-Native HRAgent</p>
          </div>
        </div>

        <nav className="flex-1 px-6 space-y-8 overflow-y-auto no-scrollbar">
          <div className="pt-4">
            <h3 className="px-4 text-[10px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-4">HỆ THỐNG</h3>
            <div className="space-y-1">
              <SidebarLink icon={LayoutDashboard} label="Tổng quan" active={activeTab === 'dashboard'} onClick={() => {setActiveTab('dashboard'); setActiveAgentId(null);}} />
              <SidebarLink icon={Database} label="Nạp dữ liệu" active={activeTab === 'data'} onClick={() => {setActiveTab('data'); setActiveAgentId(null);}} />
              <SidebarLink icon={BookOpen} label="Kho tri thức" active={activeTab === 'kb'} onClick={() => {setActiveTab('kb'); setActiveAgentId(null);}} />
            </div>
          </div>

          <div className="pt-2">
            <h3 className="px-4 text-[10px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-4">DANH SÁCH BOT</h3>
            <div className="space-y-1">
              {agents.map(agent => (
                <AgentItem 
                  key={agent.id}
                  id={agent.id}
                  initials={agent.initials}
                  name={agent.name}
                  desc={agent.desc}
                  status={agent.status}
                  active={activeAgentId === agent.id}
                  onClick={handleAgentClick}
                />
              ))}
            </div>
          </div>
          
          <div className="px-6 pt-4">
             <button className="w-full py-3 bg-blue-600/10 border border-blue-500/20 rounded-2xl text-[10px] font-black text-blue-500 uppercase tracking-widest hover:bg-blue-600 hover:text-white transition-all">
                CẤU HÌNH BOT MỚI
             </button>
          </div>
        </nav>

        <div className="p-8 border-t border-white/5 bg-black/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-600/10 border border-blue-500/20 flex items-center justify-center">
                <Users size={18} className="text-blue-500" />
              </div>
              <div className="leading-tight">
                <p className="text-sm font-bold text-white">Quản trị viên</p>
                <p className="text-[10px] text-slate-500">Super Admin</p>
              </div>
            </div>
            <Settings size={18} className="text-slate-600" />
          </div>
        </div>
      </aside>

      {/* Content Area */}
      <main className="flex-1 flex flex-col relative overflow-hidden">
        {/* Header */}
        <header className="h-20 flex items-center justify-between px-12 shrink-0 border-b border-white/5 bg-black/20 backdrop-blur-md z-10">
          <div className="relative w-[400px]">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600" size={16} />
            <input 
              type="text" 
              placeholder="Tìm kiếm phân tích..." 
              className="w-full bg-white/[0.03] border border-white/5 rounded-2xl py-2.5 pl-12 pr-4 text-xs focus:bg-white/[0.05] transition-all outline-none text-white"
            />
          </div>
          <div className="flex items-center gap-4">
            <button className="p-3 rounded-2xl hover:bg-white/5 text-slate-500 transition-all relative">
              <Bell size={20} />
              <div className="absolute top-2.5 right-2.5 w-1.5 h-1.5 bg-blue-500 rounded-full border-2 border-[#0a0c10]" />
            </button>
            <div className="w-10 h-10 rounded-full bg-slate-800 border-2 border-blue-600/50 overflow-hidden cursor-pointer active:scale-95 transition-all">
               <img src="https://ui-avatars.com/api/?name=Lê+Anh+Vũ&background=007AFF&color=fff" alt="Profile" className="w-full h-full object-cover" />
            </div>
          </div>
        </header>

        {/* Page Container */}
        <div className="flex-1 overflow-y-auto p-12 custom-scrollbar bg-[#0a0c10] relative">
          {/* Subtle Background Glows */}
          <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-blue-600/5 rounded-full blur-[120px] -z-10" />
          <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-purple-600/5 rounded-full blur-[100px] -z-10" />
          
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab + (activeAgentId || '')}
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
              className="h-full"
            >
              {renderContent()}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* System Status Footer */}
        <footer className="h-10 border-t border-white/5 bg-black/40 px-12 flex items-center justify-between text-[9px] font-bold text-slate-600 tracking-widest uppercase shrink-0">
          <div className="flex items-center gap-6">
            <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-green-500" /> HỆ THỐNG: ỔN ĐỊNH</span>
            <span className="flex items-center gap-2 text-slate-700">|</span>
            <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-blue-500" /> AI ENGINE: QWEN-2.5-MAX</span>
          </div>
          <div>© THINH LONG GROUP - xHR V2.1.0</div>
        </footer>
      </main>
    </div>
  );
}
