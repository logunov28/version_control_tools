#include <windows.h>
#include <iostream>
#include <tlhelp32.h>

using namespace std;

bool IsProcessPresent(wchar_t* szExe)
{
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(PROCESSENTRY32);
    Process32First(hSnapshot, &pe);

    if (!_wcsicmp((wchar_t*)&pe.szExeFile, szExe))
    {
        return true;
    }

    while (Process32Next(hSnapshot, &pe))
    {
        if (!_wcsicmp((wchar_t*)&pe.szExeFile, szExe))
        {
            return true;
        }
    }

    return false;
}

int main()
{
    
    ShowWindow(GetConsoleWindow(), SW_HIDE);

    TCHAR szExe[] = L"svn_client.exe";
    while (1)
    {
        if (!IsProcessPresent((wchar_t*)&szExe)) break;
        Sleep(3000);
    }

    MessageBox(0, L"SVN_client has crashed...", L"Sorry...", MB_ICONERROR | MB_OK);

    return 0;
}

