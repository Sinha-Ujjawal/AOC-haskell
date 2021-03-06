{-# LANGUAGE OverloadedStrings #-}

import Control.Monad (join)
import Data.Char (isSpace)
import qualified Data.Map.Strict as M
import Data.Maybe (mapMaybe)
import qualified Data.Text as T
import System.IO (hFlush, stdout)
import Text.Read (readMaybe)

prompt :: String -> IO String
prompt text = do
  putStr text
  hFlush stdout
  getLine

readMaybeText :: Read a => T.Text -> Maybe a
readMaybeText = readMaybe . T.unpack

counts :: (Ord a, Integral b) => [a] -> M.Map a b
counts = foldl (\m a -> M.insertWith (+) a 1 m) M.empty

type Point = (Int, Int)

data Line
  = H Int Int Int
  | V Int Int Int
  | LD Int Int Int
  | RD Int Int Int
  deriving (Show, Eq, Ord)

isDiagonal :: Line -> Bool
isDiagonal (LD {}) = True
isDiagonal (RD {}) = True
isDiagonal _ = False

points :: Line -> [Point]
points (H y x1 x2) = [(x, y) | x <- [(min x1 x2) .. (max x1 x2)]]
points (V x y1 y2) = [(x, y) | y <- [(min y1 y2) .. (max y1 y2)]]
points (LD stride x y) = [(x - s, y - s) | s <- [0 .. stride]]
points (RD stride x y) = [(x + s, y - s) | s <- [0 .. stride]]

toLine :: String -> Maybe Line
toLine =
  go
    . T.splitOn "->"
    . T.pack
    . filter (not . isSpace)
  where
    go [pair1, pair2] = go' (readMaybeText <$> T.splitOn "," pair1) (readMaybeText <$> T.splitOn "," pair2)
    go _ = Nothing

    go' [Just x1, Just y1] [Just x2, Just y2] = go'' x1 y1 x2 y2
    go' _ _ = Nothing

    go'' x1 y1 x2 y2
      | x1 == x2 = Just $ V x1 y1 y2
      | y1 == y2 = Just $ H y1 x1 x2
      | otherwise =
        let a = (y2 - y1)
            b = (x2 - x1)
         in if a == b
              then Just $ LD (abs a) (max x1 x2) (max y1 y2)
              else
                if a == (-b)
                  then Just $ RD (abs a) (min x1 x2) (max y1 y2)
                  else Nothing

toLines :: [String] -> [Line]
toLines = mapMaybe toLine

solvePart1 :: [String] -> Int
solvePart1 =
  length
    . filter ((>= 2) . snd)
    . M.toList
    . counts
    . join
    . map points
    . filter (not . isDiagonal)
    . toLines

solvePart2 :: [String] -> Int
solvePart2 =
  length
    . filter ((>= 2) . snd)
    . M.toList
    . counts
    . join
    . map points
    . toLines

main :: IO ()
main = do
  filename <- prompt "Enter file name: "
  fileLines <- lines <$> readFile filename

  let part1Ans = solvePart1 fileLines
      part2Ans = solvePart2 fileLines

  putStrLn $ "Part1: " ++ show part1Ans
  putStrLn $ "Part2: " ++ show part2Ans