name := "Page Rank Algorithm"

version := "1.0"

scalaVersion := "2.11.8"  // change this to match your scala version



libraryDependencies ++= Seq(
        "org.apache.spark" %% "spark-core" % "2.3.2",  // change version to
        // match your spark version 
        "org.scala-lang" % "scala-library" % "2.11.8",  // change this to
        // match your scala version 
        "org.apache.spark" %% "spark-mllib" % "2.3.2",
        "org.apache.spark" %% "spark-graphx" % "2.3.2"
        )

fork in run := true


