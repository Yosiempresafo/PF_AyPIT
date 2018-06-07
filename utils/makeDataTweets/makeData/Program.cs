using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using opennlp.tools.ngram;

namespace makeData
{
    class Program
    {
        public static List<string> stop = new List<string>();
        public static List<int[]> tweetsFinal = new List<int[]>();

        static void leerStopWords()
        {
            string path = @"./data/stop_en.txt";
            HashSet<string> types = new HashSet<string>();

            using (StreamReader sr = new StreamReader(path))
            {
                while (sr.Peek() >= 0)
                {
                    stop.Add(sr.ReadLine());
                }
            }
        }

        static string quitarStopWords(string token)
        {
            foreach (var item in stop)
            {
                token.Replace(item, "");
            }

            return token;
        }
        static void Main(string[] args)
        {
            //Leer archivo
            string path = @"./data/";
            string inputData = "corpusBillboard.csv";
            string exitData = "corpusBillboardCaracterizado.csv";

            HashSet<string> types = new HashSet<string>();
            leerStopWords();

            //crear vocabulario
            using (StreamReader sr = new StreamReader(path+inputData))
            {
                while (sr.Peek() >= 0)
                {
                    string line = sr.ReadLine();
                    string[] lineArray = line.Split(',');

                    //descartamos letras en blanco o etiquetas en blanco
                    if (lineArray[0] != "rank" |  lineArray[4]!=""| lineArray[4] != "NA" | lineArray[6] != "")
                    {
                        string letra = lineArray[4];

                        letra = quitarStopWords(letra); //quitar stops words
                        letra = letra.ToLower(); //minusculas

                        var ngrams = NGramGenerator.generate(letra.ToArray(), 3, "");//creamos trigramas
                        dynamic ngramsArray = ngrams.toArray();
                        
                        foreach (var token in ngramsArray)
                        {
                            types.Add(token);
                        }
                    }
                }
            }

            //caracterizar tweets
            using (StreamReader sr = new StreamReader(path+inputData))
            {
                while (sr.Peek() >= 0)
                {
                    string line = sr.ReadLine();
                    string[] lineArray = line.Split(',');

                    //descartamos tuits tipo 3
                    if (lineArray[0] != "rank" | lineArray[4] != "" | lineArray[4] != "NA" | lineArray[6] != "")
                    {
                        string letra = lineArray[4];
                        letra = quitarStopWords(letra); //quitar stops words
                        letra = letra.ToLower(); //minusculas

                        var ngrams = NGramGenerator.generate(letra.ToArray(), 3, "");//creamos trigramas
                        dynamic ngramsArray = ngrams.toArray();

                        int[] caract = new int[types.Count];
                        Array.Clear(caract, 0, caract.Length);

                        int count = 0;
                        //for (int i = 0; i < types.Count; i++)
                        foreach (var item in types)
                        {            
                            for (int j = 0; j < ngramsArray.Length; j++)
                            {
                                if (item==ngramsArray[j])
                                {
                                    caract[count] = 1;
                                }
                            }
                            count++;
                        }

                        //tweetsFinal.Add(tweetCaract);


                        using (TextWriter tw = new StreamWriter(path + exitData, true))
                        {
                            for (int i = 0; i < caract.Length; i++)
                            {
                                tw.Write(caract[i]);
                            }
                            
                            tw.Write(" " + lineArray[6]);
                            tw.WriteLine();                                                  
                        }

                    }
                }
            }
        }
    }
}
