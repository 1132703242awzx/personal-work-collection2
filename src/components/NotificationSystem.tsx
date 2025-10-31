import { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../store';
import { removeNotification } from '../store/slices/uiSlice';
import { selectNotifications } from '../store/selectors';

const NotificationSystem = () => {
  const dispatch = useAppDispatch();
  const notifications = useAppSelector(selectNotifications);

  useEffect(() => {
    // 自动移除旧通知
    notifications.forEach(notification => {
      const age = Date.now() - notification.timestamp;
      if (age > 5000) { // 5秒后自动移除
        dispatch(removeNotification(notification.id));
      }
    });
  }, [notifications, dispatch]);

  const getIcon = (type: string) => {
    switch (type) {
      case 'success': return '✅';
      case 'error': return '❌';
      case 'warning': return '⚠️';
      case 'info': return 'ℹ️';
      default: return '📢';
    }
  };

  const getColorClass = (type: string) => {
    switch (type) {
      case 'success': return 'from-green-500 to-emerald-500 border-green-500/30';
      case 'error': return 'from-red-500 to-orange-500 border-red-500/30';
      case 'warning': return 'from-yellow-500 to-orange-500 border-yellow-500/30';
      case 'info': return 'from-blue-500 to-cyan-500 border-blue-500/30';
      default: return 'from-slate-500 to-slate-600 border-slate-500/30';
    }
  };

  if (notifications.length === 0) return null;

  return (
    <div className="fixed top-20 right-4 z-50 space-y-3 max-w-sm">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`bg-gradient-to-r ${getColorClass(notification.type)} bg-opacity-10 backdrop-blur-sm border rounded-xl p-4 shadow-lg animate-fadeIn`}
        >
          <div className="flex items-start space-x-3">
            <span className="text-2xl flex-shrink-0">
              {getIcon(notification.type)}
            </span>
            <div className="flex-1">
              <p className="text-white font-medium leading-relaxed">
                {notification.message}
              </p>
            </div>
            <button
              onClick={() => dispatch(removeNotification(notification.id))}
              className="text-white/50 hover:text-white transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default NotificationSystem;
