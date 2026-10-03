import javax.tools.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

/** Compiles every sub-directory of a root, one compilation per directory. Run with: java JavaCheck.java ROOT [RELEASE] */
public class JavaCheck {
    public static void main(String[] a) throws Exception {
        JavaCompiler c = ToolProvider.getSystemJavaCompiler();
        if (c == null) { System.out.println("NOCOMPILER"); return; }
        Path root = Path.of(a[0]);
        String release = a.length > 1 ? a[1] : null;
        List<Path> dirs;
        try (Stream<Path> s = Files.list(root)) { dirs = s.filter(Files::isDirectory).sorted().collect(Collectors.toList()); }
        for (Path d : dirs) {
            List<File> files;
            try (Stream<Path> s = Files.list(d)) {
                files = s.filter(p -> p.toString().endsWith(".java")).map(Path::toFile).sorted().collect(Collectors.toList());
            }
            Path out = d.resolve("out");
            Files.createDirectories(out);
            DiagnosticCollector<JavaFileObject> dc = new DiagnosticCollector<>();
            try (StandardJavaFileManager fm = c.getStandardFileManager(dc, null, null)) {
                List<String> opts = new ArrayList<>(List.of("-d", out.toString(), "-Xlint:none"));
                if (release != null) { opts.add("--release"); opts.add(release); }
                boolean ok;
                try {
                    ok = c.getTask(new StringWriter(), fm, dc, opts, null, fm.getJavaFileObjectsFromFiles(files)).call();
                } catch (IllegalArgumentException e) {
                    if (release == null) throw e;
                    System.out.println("NOTE\trelease " + release + " not supported by this JDK; compiling with its default");
                    release = null;
                    opts = new ArrayList<>(List.of("-d", out.toString(), "-Xlint:none"));
                    ok = c.getTask(new StringWriter(), fm, dc, opts, null, fm.getJavaFileObjectsFromFiles(files)).call();
                }
                if (ok) { System.out.println("OK\t" + d.getFileName()); continue; }
                String msg = "compile error";
                for (Diagnostic<? extends JavaFileObject> x : dc.getDiagnostics()) {
                    if (x.getKind() == Diagnostic.Kind.ERROR) {
                        msg = "L" + x.getLineNumber() + ": " + x.getMessage(null).split("\n")[0];
                        break;
                    }
                }
                System.out.println("FAIL\t" + d.getFileName() + "\t" + msg);
            }
        }
    }
}
