using Microsoft.Win32.SafeHandles;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

using CLRConsole = System.Console;

namespace lockFileex
{
    #region Console
    public static class Console
    {

        public static ConsoleKeyInfo ReadKey()
        {
            return CLRConsole.ReadKey();
        }
        public static void WriteLine(string value)
        {
            if (value.IndexOf('A') > 0)
            {
                CLRConsole.ForegroundColor = System.ConsoleColor.Blue;
            }
            else 
            {
                if (value.IndexOf('B') > 0)
                {
                    CLRConsole.ForegroundColor = System.ConsoleColor.Red;
                }
                else
                { 
                    CLRConsole.ForegroundColor = System.ConsoleColor.Gray; 
                }
            }
            CLRConsole.WriteLine(value);
        }
    }
    #endregion Console

    class Program
    {
        static string path = Path.Combine(Directory.GetParent(System.IO.Directory.GetCurrentDirectory()).Parent.Parent.FullName, "ab.txt");
        public class Error_Log
        {
            public static int errors = 0;
        }

        public static void WriteA()
        {
            Console.WriteLine("Open by A");
            using (FileStream fs = File.Open(path, FileMode.Append, FileAccess.Write, FileShare.Write))
            {
                fs.LockEx(0, 10);
                Console.WriteLine("Locked by A");
                Byte[] info = new UTF8Encoding(true).GetBytes("A\r\n");
                fs.Write(info, 0, info.Length);
                fs.Flush();
                Console.WriteLine("Waiting in A ....");
                Thread.Sleep(100);
                fs.UnlockEx(0, 10);
                Console.WriteLine("Unlocked by A");
            }
            Console.WriteLine("Ended up by A");
        }

        public static void WriteB()
        {
            Console.WriteLine("Open by B");

            using (FileStream fs = File.Open(path, FileMode.Append, FileAccess.Write, FileShare.Write))
            {
                Console.WriteLine("Can lock B: " + fs.CanLockEx(0, 1000).ToString());
                fs.LockEx(0, 10);
                Console.WriteLine("Locked by B");
                Byte[] info = new UTF8Encoding(true).GetBytes("B\r\n");
                fs.Seek(0, SeekOrigin.End);
                fs.Write(info, 0, info.Length);
                fs.UnlockEx(0, 10);
                Console.WriteLine("Unlocked by B");
            }
            Console.WriteLine("Ended up by B");
        }

        public static void WriteBlock(string block, FileAccess accessPrivilages)
        {
                try
                {
                    using (FileStream fs = File.Open(path, FileMode.Append, accessPrivilages, FileShare.Write))
                        {
                            Console.WriteLine("Open by " + block[0]);
                            Console.WriteLine("Can lock " + block[0] + " : " + fs.CanLockEx(0, 1000).ToString());
                            fs.LockEx(0, 1000000);
                            Byte[] bytes = new UTF8Encoding(true).GetBytes(block + "\r\n");
                            fs.Seek(0, SeekOrigin.End);
                            fs.Write(bytes, 0, bytes.Length);
                            fs.Flush();
                            Console.WriteLine("Waiting in " + block[0] + " ....");
                            Thread.Sleep(block.Length);
                            fs.UnlockEx(0, 1000000);
                            Console.WriteLine("Unlocked by " + block[0]);
                            fs.Close();
                        }
                    }
                catch (Exception e)
                {
                    Console.WriteLine("Error while writing file.");
                    Error_Log.errors++;
                }   
        }



        static void Main(string[] args)
        {
            if (!File.Exists(path))
            {
                // Create the file.
                Console.WriteLine("Create file");
                using (FileStream fs = File.Create(path))
                {
                    Console.WriteLine("File has been created");
                }
            }

            //Excercise 1
            Console.WriteLine("------------");
            Console.WriteLine("Excercise 1");
            Console.WriteLine("Type enter to start writing single 'a' and 'b'");
            Console.ReadKey();
            Thread t1 = new Thread(WriteA);
            Thread t2 = new Thread(WriteB);
            t1.Start();
            Thread.Sleep(1);
            t2.Start();
            t1.Join(); t2.Join();


            // Excercise 2 - FileAccess.Write
            Console.WriteLine("------------");
            Console.WriteLine("Excercise 2 with file access set to Write");
            Console.WriteLine("Input lenght of the blocks");
            int blocktLenght = Convert.ToInt32(CLRConsole.ReadLine());
            Console.WriteLine("Input amount of blocks");
            int blocksAmount = Convert.ToInt32(CLRConsole.ReadLine());
            Console.WriteLine("Type enter to start writing block of a's and b's with file access set to Write");
            Console.ReadKey();
            
            Thread[] threads = new Thread[blocksAmount];
            string A = new String(Convert.ToChar(65), blocktLenght);
            string B = new String(Convert.ToChar(66), blocktLenght);

            for (int i = 0; i < blocksAmount; i++)
            {
                if (i % 2 == 0)
                    threads[i] = new Thread(() => WriteBlock(A, FileAccess.Write));
                else
                {
                    threads[i] = new Thread(() => WriteBlock(B, FileAccess.Write));
                }
                threads[i].Start();
                Thread.Sleep(100);
            }

            foreach (Thread t in threads)
            {
                t.Join();
            }

            Console.WriteLine("Amount of errors: " + Error_Log.errors.ToString());


            // Excercise 3 - FileAccess.ReadWrite
            Console.WriteLine("------------");
            Console.WriteLine("Excercise 3 with file access set to ReadWrite");
            Console.WriteLine("Type enter to start writing block of a's and b's with file access set to ReadWrite");
            Console.ReadKey();

            Thread[] threads2 = new Thread[blocksAmount];

            for (int i = 0; i < blocksAmount; i++)
            {
                if (i % 2 == 0)
                    threads2[i] = new Thread(() => WriteBlock(A, FileAccess.ReadWrite));
                else
                {
                    threads2[i] = new Thread(() => WriteBlock(B, FileAccess.ReadWrite));
                }
                threads2[i].Start();
                Thread.Sleep(100);
            }

            foreach (Thread t in threads2)
            {
                t.Join();
            }

            Console.WriteLine("Amount of errors: " + Error_Log.errors.ToString());
            Console.ReadKey();

        }
    }
}
