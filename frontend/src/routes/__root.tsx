import * as React from 'react';
import { Outlet, createRootRoute } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { Globe } from 'lucide-react';
import { useLocale, useTranslation } from '../lib/i18n-context';
import { ThemeToggle } from '../components/ThemeToggle';
import { NavigationSidebar } from '../components/NavigationSidebar';
import { useFooterVersionInfo } from '../hooks/useFooterVersionInfo';
import { DeviceProvider } from '../lib/device-context';

export const Route = createRootRoute({
  component: RootComponent,
});

export function Footer() {
  const buildBackendVersion = __BACKEND_VERSION__ || 'unknown';
  const { locale, setLocale, localeName } = useLocale();
  const t = useTranslation();
  const { backendVersion, updateInfo, showUpdateBadge, versionMismatch } =
    useFooterVersionInfo(buildBackendVersion);

  const displayedVersion = backendVersion ?? buildBackendVersion;
  const versionTitle =
    versionMismatch && backendVersion
      ? t.footer.versionMismatchDetail
          .replace('{frontend}', buildBackendVersion)
          .replace('{backend}', backendVersion)
      : t.footer.buildVersion.replace('{version}', buildBackendVersion);

  const toggleLocale = () => {
    setLocale(locale === 'en' ? 'zh' : 'en');
  };

  const handleUpdateClick = async () => {
    // 桌面端：直接触发应用内自动更新（后台静默下载，下载完弹「立即重启」），
    // 不再打开浏览器跳转到 GitHub releases 页。
    const electronAPI = (
      window as Window & {
        electronAPI?: {
          updates?: {
            checkAndDownload: () => Promise<{
              success: boolean;
              error?: string;
            }>;
          };
        };
      }
    ).electronAPI;
    if (electronAPI?.updates?.checkAndDownload) {
      await electronAPI.updates.checkAndDownload();
      return;
    }
    // 非桌面端兜底：打开 releases 页
    if (updateInfo?.release_url) {
      window.open(updateInfo.release_url, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <footer className="mt-auto border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 py-3 flex flex-col sm:flex-row items-center justify-between gap-2 text-sm">
        <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400">
          <span className="flex items-center gap-1.5" title={versionTitle}>
            V{displayedVersion}
            {__GIT_HASH__ !== 'unknown' && (
              <span className="font-mono text-xs text-slate-400 dark:text-slate-500">
                ·{__GIT_HASH__}
              </span>
            )}
            {showUpdateBadge && updateInfo?.latest_version && (
              <Badge
                variant="warning"
                className="cursor-pointer hover:opacity-80 transition-opacity"
                onClick={handleUpdateClick}
                title={t.footer.updateAvailable.replace(
                  '{version}',
                  updateInfo.latest_version
                )}
              >
                {t.footer.newVersion}
              </Badge>
            )}
            {versionMismatch && backendVersion && (
              <Badge variant="warning">{t.footer.versionMismatch}</Badge>
            )}
          </span>
          <Separator
            orientation="vertical"
            className="h-4 bg-slate-200 dark:bg-slate-700"
          />
          <button
            onClick={toggleLocale}
            className="hover:text-[#1d9bf0] transition-colors flex items-center gap-1"
            title="Switch language"
          >
            <Globe className="w-4 h-4" />
            {localeName}
          </button>
          <Separator
            orientation="vertical"
            className="h-4 bg-slate-200 dark:bg-slate-700"
          />
          <ThemeToggle />
        </div>
      </div>
    </footer>
  );
}

export function RootComponent() {
  return (
    <DeviceProvider>
      <div className="h-screen flex flex-col overflow-hidden">
        <div className="flex-1 flex overflow-hidden">
          <NavigationSidebar />
          <div className="flex-1 flex flex-col overflow-hidden">
            <div className="flex-1 overflow-auto">
              <Outlet />
            </div>
            <Footer />
          </div>
        </div>
        {__DEVTOOLS_ENABLED__ && (
          <TanStackRouterDevtools position="bottom-right" />
        )}
      </div>
    </DeviceProvider>
  );
}
