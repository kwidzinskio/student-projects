using Microsoft.Win32.SafeHandles;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;



namespace lockFileex
{
    public static class LockExtension
    {
        [StructLayout(LayoutKind.Sequential)]
        public struct OVERLAPPED
        {
            public uint internalLow;
            public uint internalHigh;
            public uint offsetLow;
            public uint offsetHigh;
            public IntPtr hEvent;
        }

        [DllImport("Kernel32.dll", SetLastError = true)]
        private static extern bool LockFileEx(SafeFileHandle handle, uint flags, uint reserved, uint countLow, uint countHigh, ref OVERLAPPED overlapped);

        [DllImport("Kernel32.dll", SetLastError = true)]
        private static extern bool UnlockFileEx(SafeFileHandle handle, uint reserved, uint countLow, uint countHigh, ref OVERLAPPED overlapped);

        [DllImport("kernel32.dll")]
        static extern uint GetLastError();

        private const uint LOCKFILE_FAIL_IMMEDIATELY = 0x00000001; //dla flase ERROR_LOCK_VIOLATION
        private const uint LOCKFILE_EXCLUSIVE_LOCK = 0x00000002;
        private const uint ERROR_LOCK_VIOLATION = 33;

        public static void LockEx(this FileStream fs, ulong offset, ulong count)
        {
            uint countLow = (uint)count;
            uint countHigh = (uint)(count >> 32);

            OVERLAPPED overlapped = new OVERLAPPED()
            {
                internalLow = 0,
                internalHigh = 0,
                offsetLow = (uint)offset,
                offsetHigh = (uint)(offset >> 32),
                hEvent = IntPtr.Zero,
            };

            if (!LockFileEx(fs.SafeFileHandle, LOCKFILE_EXCLUSIVE_LOCK, 0, countLow, countHigh, ref overlapped))
            {
                //TODO: throw an exception
            }
        }

        public static bool TryLockEx(this FileStream fs, ulong offset, ulong count)
        {
            uint countLow = (uint)count;
            uint countHigh = (uint)(count >> 32);

            OVERLAPPED overlapped = new OVERLAPPED()
            {
                internalLow = 0,
                internalHigh = 0,
                offsetLow = (uint)offset,
                offsetHigh = (uint)(offset >> 32),
                hEvent = IntPtr.Zero,
            };

            if (!LockFileEx(fs.SafeFileHandle, LOCKFILE_EXCLUSIVE_LOCK | LOCKFILE_FAIL_IMMEDIATELY, 0, countLow,
                countHigh, ref overlapped))
            {
                if (GetLastError() == ERROR_LOCK_VIOLATION)
                {
                    return false;
                }
                else
                {
                    //TODO throw
                }
            }           
            return true;
        }


        public static bool CanLockEx(this FileStream fs, ulong offset, ulong count)
        {
            uint countLow = (uint)count;
            uint countHigh = (uint)(count >> 32);

            OVERLAPPED overlapped = new OVERLAPPED()
            {
                internalLow = 0,
                internalHigh = 0,
                offsetLow = (uint)offset,
                offsetHigh = (uint)(offset >> 32),
                hEvent = IntPtr.Zero,
            };

            if (!LockFileEx(fs.SafeFileHandle, LOCKFILE_EXCLUSIVE_LOCK | LOCKFILE_FAIL_IMMEDIATELY, 0, countLow,
                countHigh, ref overlapped))
            {
                if (GetLastError() == ERROR_LOCK_VIOLATION)
                {
                    return false;
                }
                else
                {
                    //TODO throw
                }
            }
            else
            {
                //if true unlock, small workaround !!!
                UnlockEx(fs, offset, count);
            }
            return true;
        }


        public static void UnlockEx(this FileStream fs, ulong offset, ulong count)
        {
            uint countLow = (uint)count;
            uint countHigh = (uint)(count >> 32);

            OVERLAPPED overlapped = new OVERLAPPED()
            {
                internalLow = 0,
                internalHigh = 0,
                offsetLow = (uint)offset,
                offsetHigh = (uint)(offset >> 32),
                hEvent = IntPtr.Zero,
            };

            if (!UnlockFileEx(fs.SafeFileHandle, 0, countLow, countHigh, ref overlapped))
            {
                //TODO: throw an exception
            }
        }


    }
}
