import { DashboardContainer } from '@/components/dashboard';
import { ChatContainer } from '@/components/chat';

export function MainLayout() {
  return (
    <div className="flex h-screen">
      {/* Dashboard - 65% */}
      <div className="w-[65%] border-r border-gray-200 overflow-hidden bg-gray-50">
        <DashboardContainer />
      </div>
      {/* Chat - 35% */}
      <div className="w-[35%] overflow-hidden">
        <ChatContainer />
      </div>
    </div>
  );
}
