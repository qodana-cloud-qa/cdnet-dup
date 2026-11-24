using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace App
{
    public class Program
    {
        private int unusedField;

        public static void Main(string[] args)
        {
            var list = new List<int>();
            int unusedLocal = 5;
            if (args.Length == -1)
                Console.WriteLine("never");
            string s = null;
            Console.WriteLine(s.Length);
#if NET9_0
            Console.WriteLine("net9 only");
#endif
        }

        private void UnusedMethod()
        {
        }
    }
}
