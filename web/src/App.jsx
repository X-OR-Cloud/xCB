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
  Activity,
  Sun,
  Moon,
  Leaf
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

const DashboardHC = ({ stats, riskData }) => (
  <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
    <div className="flex flex-col gap-1">
      <h2 className="text-3xl font-black text-[var(--text-main)] tracking-tight">Trung tâm Điều hành Hành chính Công xCB</h2>
      <p className="text-[var(--text-muted)] text-sm">Giám sát xử lý hồ sơ và hỗ trợ nghiệp vụ cán bộ công chức địa phương.</p>
    </div>

    {/* Top Row: KPIs Hành chính */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[
        { label: "Hồ sơ tiếp nhận", value: stats.ho_so_tiep_nhan || "1,284", change: stats.tiep_nhan_change || "+8.3%", color: "blue", progress: 65, icon: FileText },
        { label: "Tỉ lệ đúng hạn", value: stats.ti_le_dung_han || "94.2%", change: stats.dung_han_change || "+2.1%", color: "blue", progress: 94, icon: ShieldCheck },
        { label: "Đang chờ xử lý", value: stats.dang_cho || "187", change: stats.cho_change || "-5.4%", color: "purple", progress: 15, icon: Clock },
        { label: "Hồ sơ quá hạn", value: stats.qua_han || "23", change: stats.qua_han_change || "-12.0%", color: "red", progress: 5, icon: AlertCircle }
      ].map((kpi, i) => (
        <div key={i} className={`glass-card p-6 border-[var(--border-color)] bg-[#121212]/30 relative group overflow-hidden`}>
          <div className="flex justify-between items-start mb-6">
            <div className={`p-3 rounded-xl ${
              kpi.color === 'blue' ? 'bg-cyan-500/10 text-cyan-500' : 
              kpi.color === 'purple' ? 'bg-purple-500/10 text-purple-500' : 'bg-red-500/10 text-red-500'
            }`}>
              <kpi.icon size={20} />
            </div>
            <span className={`text-[10px] font-black ${
               kpi.color === 'red' ? (kpi.change.startsWith('-') ? 'text-green-500' : 'text-red-500') :
               (kpi.change.startsWith('+') ? 'text-green-500' : 'text-slate-500')
            }`}>{kpi.change}</span>
          </div>
          <p className="text-[9px] font-bold text-slate-500 uppercase tracking-[0.2em] mb-2">{kpi.label}</p>
          <h3 className={`text-2xl font-black text-white ${kpi.color === 'blue' ? 'neon-text-cyan' : kpi.color === 'purple' ? 'neon-text-purple' : ''}`}>{kpi.value}</h3>
          
          <div className="mt-6 space-y-2">
            <div className="flex justify-between items-center text-[8px] font-bold text-slate-600 uppercase tracking-widest">
              <span>Mức độ xử lý</span>
              <span>{kpi.progress}%</span>
            </div>
            <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
               <motion.div 
                 initial={{ width: 0 }}
                 animate={{ width: `${kpi.progress}%` }}
                 className={`h-full rounded-full ${
                  kpi.color === 'blue' ? 'bg-cyan-500 shadow-[0_0_10px_#00f2ff]' : 
                  kpi.color === 'purple' ? 'bg-purple-500 shadow-[0_0_10px_#bc13fe]' : 'bg-red-500 shadow-[0_0_10px_#ff4444]'
                }`} />
            </div>
          </div>
        </div>
      ))}
    </div>

    {/* Middle Row: Vietnam Map & AI Insights */}
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
      {/* AI Performance Chart */}
      <div className="lg:col-span-8 glass-card p-8 bg-[#121212]/40 relative overflow-hidden group">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h3 className="text-xl font-black text-white neon-text-cyan flex items-center gap-3">
              <TrendingUp className="text-[var(--neon-cyan)]" size={20} />
              Biểu đồ Hiệu suất Hỗ trợ AI
            </h3>
            <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider mt-1">Năng suất xử lý nghiệp vụ theo thời gian & Agent</p>
          </div>
          <div className="flex gap-2">
            {['Ngày', 'Tháng', 'Năm'].map(p => (
              <button key={p} className={`px-3 py-1 rounded-lg text-[9px] font-bold uppercase tracking-widest border transition-all ${p === 'Tháng' ? 'bg-cyan-500/20 border-cyan-500/50 text-cyan-400' : 'border-white/5 text-slate-500 hover:border-white/20'}`}>
                {p}
              </button>
            ))}
          </div>
        </div>

        <div className="h-[450px] w-full bg-black/40 rounded-[2.5rem] p-10 flex flex-col justify-between border border-white/5 relative">
           <div className="flex-1 flex items-end gap-4 mb-8 relative">
              {/* Line Chart Overlay (Total Tasks) */}
              <svg className="absolute inset-0 w-full h-full pointer-events-none z-10" preserveAspectRatio="none">
                <motion.path
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 1 }}
                  transition={{ duration: 2, ease: "easeInOut" }}
                  d={`M ${[
                    { val: 852, total: 1202 }, { val: 641, total: 1400 }, { val: 1420, total: 1650 }, 
                    { val: 453, total: 1490 }, { val: 742, total: 1100 }, { val: 561, total: 1000 }, 
                    { val: 1854, total: 1980 }, { val: 921, total: 1350 }, { val: 618, total: 850 }
                  ].map((d, i) => `${(i * 11.1) + 5.5}% ${(1 - (d.total / 2000)) * 100}%`).join(' L ')}`}
                  fill="none"
                  stroke="rgba(255, 255, 255, 0.2)"
                  strokeWidth="2"
                  strokeDasharray="4 4"
                />
                {[
                  { val: 852, total: 1202 }, { val: 641, total: 1400 }, { val: 1420, total: 1650 }, 
                  { val: 453, total: 1490 }, { val: 742, total: 1100 }, { val: 561, total: 1000 }, 
                  { val: 1854, total: 1980 }, { val: 921, total: 1350 }, { val: 618, total: 850 }
                ].map((d, i) => (
                  <circle 
                    key={i} 
                    cx={`${(i * 11.1) + 5.5}%`} 
                    cy={`${(1 - (d.total / 2000)) * 100}%`} 
                    r="3" 
                    fill="white" 
                    className="opacity-40"
                  />
                ))}
              </svg>

              {[
                { label: 'PL', val: 852, total: 1202, max: 2000, color: 'cyan' },
                { label: 'GD', val: 641, total: 1400, max: 2000, color: 'blue' },
                { label: 'BH', val: 1420, total: 1650, max: 2000, color: 'purple' },
                { label: 'TN', val: 453, total: 1490, max: 2000, color: 'cyan' },
                { label: 'NN', val: 742, total: 1100, max: 2000, color: 'blue' },
                { label: 'CN', val: 561, total: 1000, max: 2000, color: 'purple' },
                { label: 'HC', val: 1854, total: 1980, max: 2000, color: 'cyan' },
                { label: 'DN', val: 921, total: 1350, max: 2000, color: 'blue' },
                { label: 'GM', val: 618, total: 850, max: 2000, color: 'purple' },
              ].map((item, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-4 h-full group z-0">
                  <div className="flex-1 w-full bg-white/[0.02] rounded-2xl relative flex items-end justify-center border border-white/5 group-hover:border-cyan-500/30 transition-all">
                    <motion.div 
                      initial={{ height: 0 }}
                      animate={{ height: `${(item.val / item.max) * 100}%` }}
                      transition={{ delay: i * 0.1, duration: 1 }}
                      className={`w-full bg-gradient-to-t rounded-t-xl ${
                        item.color === 'cyan' ? 'from-cyan-600/40 to-cyan-400/60 shadow-[0_0_20px_rgba(0,242,255,0.2)]' :
                        item.color === 'purple' ? 'from-purple-600/40 to-purple-400/60 shadow-[0_0_20px_rgba(188,19,254,0.2)]' :
                        'from-blue-600/40 to-blue-400/60 shadow-[0_0_20px_rgba(37,99,235,0.2)]'
                      }`}
                    />
                    <div className="absolute top-4 opacity-0 group-hover:opacity-100 transition-opacity text-[8px] font-black text-white whitespace-nowrap bg-black/80 px-2 py-1 rounded border border-white/10 z-20">
                      AI: {item.val} | Tổng: {item.total}
                    </div>
                  </div>
                  <span className="text-[10px] font-bold text-slate-500 group-hover:text-cyan-400 transition-colors uppercase tracking-widest">{item.label}</span>
                </div>
              ))}
           </div>
           
           <div className="h-px w-full bg-white/5 mb-6" />
           
           <div className="flex justify-between items-center">
              <div className="flex gap-8">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-cyan-500 shadow-[0_0_10px_#00f2ff]" />
                  <span className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">AI Xử lý</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-12 h-0.5 border-t border-dashed border-white/40" />
                  <span className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">Tổng nhiệm vụ</span>
                </div>
              </div>
              <p className="text-[9px] font-bold text-slate-600 uppercase tracking-wide">Cập nhật: 10 giây trước • xAI-Insight</p>
           </div>
        </div>
      </div>

      {/* Strategic Alerts & AI Insights */}
      <div className="lg:col-span-4 space-y-8">
        <div className="glass-morphism p-6 relative overflow-hidden group">
           <h3 className="text-sm font-black text-white mb-8 flex items-center gap-3">
             <div className="w-1.5 h-1.5 rounded-full bg-red-500 animate-ping" />
             Cảnh báo & Chỉ đạo
           </h3>
           <div className="space-y-4">
              <div className="bg-red-500/5 border border-red-500/10 rounded-2xl p-4">
                 <p className="text-[9px] font-black text-red-500 uppercase tracking-widest mb-1">CẢNH BÁO QUÁ HẠN</p>
                 <p className="text-xs text-slate-400 font-medium font-mono tracking-tight">Lĩnh vực Đất đai: 12 hồ sơ chưa xử lý đúng hạn.</p>
              </div>
              <div className="bg-cyan-500/5 border border-cyan-500/10 rounded-2xl p-4">
                 <p className="text-[9px] font-black text-cyan-400 uppercase tracking-widest mb-1">CHÍNH SÁCH MỚI</p>
                 <p className="text-xs text-slate-400 font-medium font-mono tracking-tight">Cập nhật Nghị định 123/2024 về dịch vụ công.</p>
              </div>
           </div>
        </div>

        <div className="glass-morphism p-6 bg-gradient-to-br from-[#bc13fe]/5 to-transparent relative overflow-hidden">
           <h3 className="text-sm font-black text-white mb-6 flex items-center gap-3">
             <Bot size={18} className="text-[var(--neon-purple)]" />
             Trợ lý xAI-GM Gợi ý
           </h3>
           <div className="space-y-4">
              <p className="text-[10px] text-slate-500 leading-relaxed italic">"Dữ liệu cho thấy tỉ lệ hồ sơ Bảo hiểm tăng 15%. Đề xuất bổ sung tri thức nDD-2024 cho xAI-BH để tối ưu phản hồi."</p>
           </div>
        </div>
      </div>
    </div>

    {/* Bottom Row: Field Analysis */}
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
       <div className="lg:col-span-12 glass-card p-8 bg-[#121212]/40">
          <div className="flex justify-between items-center mb-8">
             <h3 className="text-lg font-bold text-white uppercase tracking-wider">Phân tích hồ sơ theo lĩnh vực</h3>
             <span className="text-[10px] font-bold text-slate-500">6 THÁNG GẦN NHẤT</span>
          </div>
           <div className="h-64 w-full bg-black/20 rounded-[2.5rem] p-8 relative overflow-hidden border border-white/5 mt-4">
              <svg className="absolute inset-0 w-full h-full pointer-events-none" preserveAspectRatio="none">
                <motion.path
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 1 }}
                  transition={{ duration: 2, ease: "easeInOut" }}
                  d={`M ${riskData.map((d, i) => `${(i * (100 / (riskData.length - 1)))}% ${(1 - (d.risk / 100)) * 100}%`).join(' L ')}`}
                  fill="none"
                  stroke="url(#neonGradient)"
                  strokeWidth="3"
                />
                <defs>
                  <linearGradient id="neonGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#00f2ff" />
                    <stop offset="50%" stopColor="#bc13fe" />
                    <stop offset="100%" stopColor="#00f2ff" />
                  </linearGradient>
                </defs>
              </svg>

              <div className="absolute inset-0 flex justify-between px-8">
                {riskData.map((item, i) => (
                  <div key={i} className="flex flex-col items-center justify-between h-full group z-10">
                    <div className="relative h-full flex flex-col items-center w-8">
                      <motion.div 
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: i * 0.1 }}
                        className="w-3 h-3 rounded-full bg-white shadow-[0_0_15px_#fff] border-2 border-cyan-500 cursor-pointer group-hover:scale-125 transition-all absolute"
                        style={{ top: `${(1 - (item.risk / 100)) * 100}%` }}
                      />
                      <div 
                        className="absolute opacity-0 group-hover:opacity-100 transition-opacity bg-black/80 backdrop-blur-md border border-white/10 px-2 py-1 rounded text-[10px] font-black text-white whitespace-nowrap z-20"
                        style={{ top: `${(1 - (item.risk / 100)) * 100 - 15}%` }}
                      >
                        {item.risk} hồ sơ
                      </div>
                    </div>
                    <span className="text-[10px] font-bold text-slate-500 group-hover:text-cyan-400 transition-colors uppercase tracking-widest mt-auto pb-4">{item.dept.substring(0, 2)}</span>
                  </div>
                ))}
              </div>
           </div>
        </div>
     </div>
  </motion.div>
);


const DataManager = ({ onUpload }) => {
  const fileInputRef = useRef(null);
  
  // Mock data for storage and monthly usage
  const storageStats = {
    total: 15.0, // TB
    used: 5.2,   // TB
    percentage: 34.6,
    monthlyUsage: [0.9, 1.4, 1.1, 1.8, 2.4, 2.1], // TB per month for last 6 months
    months: ['T10', 'T11', 'T12', 'T01', 'T02', '03']
  };

  // Mock data for processing queue
  const mockFiles = [
    { ten_file: "NGHI_DINH_123_2024_CHINH_PHU.pdf", dung_luong: 4500, tien_do_ocr: 100, tien_do_vector: 100, status: 'completed' },
    { ten_file: "HO_SO_CAP_PHEP_XD_PHUONG_1.docx", dung_luong: 2100, tien_do_ocr: 100, tien_do_vector: 85, status: 'processing' },
    { ten_file: "SCAN_DON_XIN_GIA_HAN_DAT_02.jpg", dung_luong: 12500, tien_do_ocr: 65, tien_do_vector: 0, status: 'ocr_scanning' },
    { ten_file: "QUYET_DINH_PHAN_CAP_QUYEN_HAN.pdf", dung_luong: 8500, tien_do_ocr: 0, tien_do_vector: 0, status: 'queued' }
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
          <h2 className="text-3xl font-bold text-[var(--text-main)] tracking-tight">Trung tâm Nạp dữ liệu xCB</h2>
          <p className="text-[var(--text-muted)] text-sm">Quản lý nạp tri thức nghiệp vụ cho các AI Agents địa phương</p>
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
             <h3 className="text-sm font-bold text-[var(--text-main)] uppercase tracking-widest">Dung lượng Lưu trữ</h3>
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
               <h3 className="text-sm font-bold text-[var(--text-main)] uppercase tracking-widest">Tình hình sử dụng trong tháng (TB)</h3>
             </div>
             <div className="px-3 py-1 bg-white/5 rounded-lg text-slate-500 text-[10px] font-bold">+24% so với năm ngoái</div>
          </div>
          <div className="h-48 flex items-end gap-4">
            {storageStats.monthlyUsage.map((val, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-2 group h-full">
                <div className="w-full h-full bg-blue-600/10 rounded-t-lg relative flex items-end justify-center overflow-hidden">
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
                <p className="text-sm font-bold text-blue-500 font-mono">/Users/XCB/Documents/Administrative_Docs</p>
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
          <h3 className="text-xl font-bold text-[var(--text-main)]">Hàng đợi Xử lý (Mockdata)</h3>
          <span className="px-3 py-1 bg-[var(--border-color)] rounded-lg text-[10px] font-bold text-[var(--text-muted)] uppercase tracking-widest">Đang xử lý: 3</span>
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
          <h2 className="text-4xl font-black text-[var(--text-main)] tracking-tight">Cơ sở Tri thức</h2>
          <p className="text-[var(--text-muted)] text-sm">Quản lý bộ sưu tập vector và chỉ mục tìm kiếm ngữ nghĩa</p>
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

      {/* Knowledge Distribution Chart */}
      <div className="glass-card p-8 bg-blue-500/[0.02]">
        <div className="flex justify-between items-center mb-10">
          <div>
            <h3 className="text-xl font-bold text-white uppercase tracking-wider mb-2">Thống kê Tri thức theo Lĩnh vực</h3>
            <p className="text-xs text-slate-500">Phân bổ tài liệu nghiệp vụ phục vụ xAI-Agents</p>
          </div>
          <span className="px-4 py-2 bg-blue-600/10 text-blue-500 rounded-xl text-[10px] font-black tracking-widest uppercase">Cập nhật theo thời gian thực</span>
        </div>

        <div className="space-y-6">
           {[
             { label: 'Hành chính Công', docs: 3100, color: '#3b82f6' },
             { label: 'Pháp lý - Luật', docs: 2450, color: '#06b6d4' },
             { label: 'Bảo hiểm XH', docs: 1820, color: '#10b981' },
             { label: 'Tài nguyên & Đất đai', docs: 1640, color: '#14b8a6' },
             { label: 'Doanh nghiệp', docs: 1250, color: '#6366f1' },
             { label: 'Giáo dục', docs: 980, color: '#f59e0b' },
             { label: 'Công nghiệp', docs: 890, color: '#ec4899' },
             { label: 'Nông nghiệp', docs: 720, color: '#84cc16' }
           ].map((item, i) => (
             <div key={i} className="space-y-2 group">
               <div className="flex justify-between items-end">
                 <span className="text-xs font-bold text-slate-400 group-hover:text-white transition-colors">{item.label}</span>
                 <span className="text-xs font-black text-white">{item.docs.toLocaleString()} <span className="text-[10px] font-normal text-slate-500">tài liệu</span></span>
               </div>
               <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                 <motion.div 
                   initial={{ width: 0 }}
                   animate={{ width: `${(item.docs / 3100) * 100}%` }}
                   transition={{ delay: i * 0.1, duration: 1 }}
                   style={{ backgroundColor: item.color }}
                   className="h-full rounded-full shadow-[0_0_15px_rgba(0,0,0,0.3)] group-hover:brightness-125 transition-all"
                 />
               </div>
             </div>
           ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: Collections */}
        <div className="lg:col-span-8 space-y-8">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold text-[var(--text-main)]">Bộ sưu tập Tri thức</h3>
            <div className="flex gap-2">
              <button className="p-2 rounded-lg bg-blue-600/20 text-blue-500 border border-blue-500/20"><LayoutDashboard size={18} /></button>
              <button className="p-2 rounded-lg hover:bg-white/5 text-slate-600"><MoreVertical size={18} className="rotate-90" /></button>
            </div>
          </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[
                { id: "phap_ly", name: "Pháp Luật", docs: 2450, icon: ShieldCheck, color: "blue", status: "RAG HOẠT ĐỘNG" },
                { id: "bao_hiem", name: "Bảo Hiểm Xã Hội", docs: 1820, icon: ShieldCheck, color: "green", status: "MẬT ĐỘ CAO" },
                { id: "dat_dai", name: "Tài Nguyên - Đất Đai", docs: 1640, icon: Globe, color: "teal", status: "RAG HOẠT ĐỘNG" },
                { id: "hanh_chinh", name: "Hành Chính Công", docs: 3100, icon: FileText, color: "blue", status: "MẬT ĐỘ CAO" },
                { id: "giao_duc", name: "Giáo Dục", docs: 980, icon: GraduationCap, color: "amber", status: "RAG HOẠT ĐỘNG" },
                { id: "nong_nghiep", name: "Nông Nghiệp", docs: 720, icon: Leaf, color: "lime", status: "ĐANG XỬ LÝ" }
              ].map((col) => (
                <div key={col.id} className={`glass-card p-8 group cursor-pointer hover:border-${col.color}-500/30 transition-all`}>
                  <div className="flex justify-between items-start mb-8">
                    <div className="flex gap-4">
                      <div className={`w-12 h-12 rounded-2xl bg-${col.color}-500/10 flex items-center justify-center border border-${col.color}-500/20`}>
                        <col.icon className={`text-${col.color}-500`} size={24} />
                      </div>
                      <div>
                        <h4 className="text-lg font-bold text-[var(--text-main)]">{col.name}</h4>
                        <p className="text-[10px] text-slate-600 font-mono">{col.id}</p>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-lg bg-${col.color}-500/10 text-[9px] font-black text-${col.color}-500 uppercase tracking-widest border border-${col.color}-500/20`}>{col.status}</span>
                  </div>
                  <div className="flex gap-10">
                    <div>
                      <p className="text-[9px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-1">TÀI LIỆU</p>
                      <p className="text-lg font-black text-slate-300">{col.docs}</p>
                    </div>
                    <div>
                      <p className="text-[9px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-1">TRẠNG THÁI</p>
                      <p className="text-lg font-black text-green-500">Sẵn sàng</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
        </div>

        {/* Right: Semantic Search Preview */}
        <div className="lg:col-span-4 space-y-6">
          <div className="glass-card p-8 bg-blue-500/[0.02] border-blue-500/10">
            <h3 className="text-lg font-bold text-[var(--text-main)] flex items-center gap-3 mb-8">
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
                  <p className="text-xs text-slate-400 italic">"Quy định về cấp giấy phép xây dựng nhà ở riêng lẻ tại nông thôn?"</p>
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
                    <span className="text-[10px] font-bold uppercase tracking-widest">LUAT_XAY_DUNG_2024_MOI.PDF</span>
                  </div>
                  <p className="text-[11px] leading-relaxed text-slate-400">
                    "Theo Điều 89 Luật Xây dựng, công trình xây dựng nhà ở riêng lẻ tại nông thôn thuộc khu vực chưa có quy hoạch phát triển đô thị được miễn giấy phép xây dựng..."
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
            <h3 className="font-bold text-[var(--text-main)] text-lg">{agent.name}</h3>
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
              <span className="text-[10px] font-bold text-[var(--text-muted)] uppercase tracking-widest">Đang phản hồi</span>
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
                  : 'bg-[var(--sidebar-bg)] text-[var(--text-main)] border border-[var(--border-color)] rounded-tl-none shadow-sm'
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
  const [dashboardStats, setDashboardStats] = useState({
    ho_so_tiep_nhan: "1,452",
    ti_le_dung_han: "96.5%",
    dang_cho: "124",
    qua_han: "12"
  });
  const [riskData, setRiskData] = useState([
    { dept: 'Pháp lý', risk: 65 },
    { dept: 'Giáo dục', risk: 45 },
    { dept: 'Bảo hiểm', risk: 85 },
    { dept: 'Tài nguyên', risk: 30 },
    { dept: 'Nông nghiệp', risk: 70 },
    { dept: 'Công nghiệp', risk: 55 },
    { dept: 'Hành chính', risk: 95 },
    { dept: 'Doanh nghiệp', risk: 80 },
    { dept: 'Giám sát', risk: 60 },
  ]);
  const [files, setFiles] = useState([]);
  const [collections, setCollections] = useState([]);
  const [isDark, setIsDark] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('theme');
      if (saved) return saved === 'dark';
      return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return true;
  });

  // Apply theme class
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDark]);

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
    { id: 'pl', initials: 'PL', name: 'xAI-PL', desc: 'Pháp lý', status: 'online' },
    { id: 'gd', initials: 'GD', name: 'xAI-GD', desc: 'Giáo dục', status: 'online' },
    { id: 'bh', initials: 'BH', name: 'xAI-BH', desc: 'Bảo hiểm', status: 'online' },
    { id: 'tn', initials: 'TN', name: 'xAI-TN', desc: 'Tài nguyên', status: 'online' },
    { id: 'nn', initials: 'NN', name: 'xAI-NN', desc: 'Nông nghiệp', status: 'away' },
    { id: 'cn', initials: 'CN', name: 'xAI-CN', desc: 'Công nghiệp', status: 'online' },
    { id: 'hc', initials: 'HC', name: 'xAI-HC', desc: 'Hành chính công', status: 'online' },
    { id: 'dn', initials: 'DN', name: 'xAI-DN', desc: 'DN & Đầu tư', status: 'online' },
    { id: 'gm', initials: 'AI', name: 'xAI-GM', desc: 'Giám sát hệ thống', status: 'online' },
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
      case 'dashboard': return <DashboardHC stats={dashboardStats} riskData={riskData} />;
      case 'data': return <DataManager onUpload={handleUpload} />;
      case 'kb': return <KnowledgeBase collections={collections} />;
      default: return <DashboardHC stats={dashboardStats} riskData={riskData} />;
    }
  };

  return (
    <div className="flex h-screen bg-[var(--bg-main)] text-[var(--text-main)] font-sans selection:bg-blue-500/30 overflow-hidden transition-colors duration-500">
      {/* Sidebar */}
      <aside className="w-72 bg-[var(--sidebar-bg)] border-r border-[var(--border-color)] flex flex-col shrink-0 transition-colors duration-500">
        <div className="p-10 flex items-center gap-4">
          <div className="w-12 h-12 flex items-center justify-center">
            <img src="/logo.png" alt="xCB Logo" className="w-full h-full object-contain" />
          </div>
          <div className="leading-tight">
            <h1 className="font-black text-2xl tracking-tighter text-[var(--text-main)]">xCB</h1>
            <p className="text-[9px] font-bold text-slate-500 tracking-widest uppercase">AI Công Chức Địa Phương</p>
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
              className="w-full bg-[var(--sidebar-bg)] border border-[var(--border-color)] rounded-2xl py-2.5 pl-12 pr-4 text-xs focus:ring-2 focus:ring-blue-500/20 transition-all outline-none text-[var(--text-main)]"
            />
          </div>
          <div className="flex items-center gap-2">
            <button 
              onClick={() => setIsDark(!isDark)}
              className="p-3 rounded-2xl hover:bg-slate-500/10 text-slate-500 transition-all active:scale-90"
            >
              {isDark ? <Sun size={20} className="text-amber-400" /> : <Moon size={20} className="text-slate-700" />}
            </button>
            <button className="p-3 rounded-2xl hover:bg-slate-500/10 text-slate-500 transition-all relative">
              <Bell size={20} />
              <div className="absolute top-2.5 right-2.5 w-1.5 h-1.5 bg-blue-500 rounded-full border-2 border-[var(--bg-main)]" />
            </button>
            <div className="w-10 h-10 rounded-full bg-slate-800 border-2 border-blue-600/50 overflow-hidden cursor-pointer active:scale-95 transition-all">
               <img src="https://ui-avatars.com/api/?name=Lê+Anh+Vũ&background=007AFF&color=fff" alt="Profile" className="w-full h-full object-cover" />
            </div>
          </div>
        </header>

        {/* Page Container */}
        <div className="flex-1 overflow-y-auto p-12 custom-scrollbar bg-[var(--bg-main)] relative transition-colors duration-500">
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
        <footer className="h-10 border-t border-[var(--border-color)] bg-[var(--sidebar-bg)] px-12 flex items-center justify-between text-[9px] font-bold text-slate-500 tracking-widest uppercase shrink-0 transition-colors duration-500">
          <div className="flex items-center gap-6">
            <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-green-500" /> HỆ THỐNG: ỔN ĐỊNH</span>
            <span className="flex items-center gap-2 text-slate-700">|</span>
            <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-blue-500" /> AI ENGINE: QWEN-2.5-MAX</span>
          </div>
          <div>© NỀN TẢNG xCB V1.0.0</div>
        </footer>
      </main>
    </div>
  );
}
