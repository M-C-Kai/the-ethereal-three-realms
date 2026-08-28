.class public final La/c/x;
.super Ljava/lang/Object;


# static fields
.field public static a:I

.field public static b:I

.field public static c:I

.field public static d:I

.field public static e:[I

.field public static f:Lpmsj/work/a/i;

.field public static g:Lpmsj/work/a/i;

.field static final h:[B

.field static final i:[B

.field private static j:Ljava/util/Random;

.field private static k:Lpmsj/work/a/i;

.field private static l:Lpmsj/work/a/i;

.field private static m:Lpmsj/work/a/i;

.field private static n:I

.field private static o:I

.field private static p:I

.field private static q:Ljava/util/Vector;

.field private static r:Ljava/util/Vector;

.field private static s:Ljava/util/Vector;


# direct methods
.method static constructor <clinit>()V
    .locals 6

    const/16 v0, 0x978

    const/16 v5, 0x9

    const/16 v4, 0x64

    const/4 v3, 0x0

    sput v0, La/c/x;->a:I

    sput v0, La/c/x;->b:I

    sget v0, La/c/x;->a:I

    sput v0, La/c/x;->d:I

    const/4 v0, 0x0

    sput-object v0, La/c/x;->e:[I

    new-instance v0, Ljava/util/Random;

    invoke-direct {v0}, Ljava/util/Random;-><init>()V

    sput-object v0, La/c/x;->j:Ljava/util/Random;

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x54d8bb

    invoke-direct {v0, v1, v3}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, La/c/x;->f:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x147790

    invoke-direct {v0, v1, v3}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, La/c/x;->k:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x147664

    invoke-direct {v0, v1, v3}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, La/c/x;->l:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    sget-object v1, Lpmsj/work/a/c;->aN:[I

    const/4 v2, 0x1

    aget v1, v1, v2

    invoke-direct {v0, v1, v3}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, La/c/x;->m:Lpmsj/work/a/i;

    new-array v0, v5, [B

    fill-array-data v0, :array_0

    sput-object v0, La/c/x;->h:[B

    new-array v0, v5, [B

    fill-array-data v0, :array_1

    sput-object v0, La/c/x;->i:[B

    sput v4, La/c/x;->n:I

    sput v4, La/c/x;->o:I

    sput v4, La/c/x;->p:I

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    sput-object v0, La/c/x;->q:Ljava/util/Vector;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    sput-object v0, La/c/x;->r:Ljava/util/Vector;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    sput-object v0, La/c/x;->s:Ljava/util/Vector;

    return-void

    nop

    :array_0
    .array-data 1
        0x0t
        -0x1t
        -0x1t
        -0x1t
        0x0t
        0x1t
        0x1t
        0x1t
        0x0t
    .end array-data

    nop

    :array_1
    .array-data 1
        0x1t
        0x1t
        0x0t
        -0x1t
        -0x1t
        -0x1t
        0x0t
        0x1t
        0x0t
    .end array-data
.end method

.method public constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static a(IIII)B
    .locals 1

    if-ge p0, p2, :cond_2

    if-ge p1, p3, :cond_0

    const/4 v0, 0x7

    :goto_0
    return v0

    :cond_0
    if-le p1, p3, :cond_1

    const/4 v0, 0x5

    goto :goto_0

    :cond_1
    const/4 v0, 0x6

    goto :goto_0

    :cond_2
    if-le p0, p2, :cond_5

    if-ge p1, p3, :cond_3

    const/4 v0, 0x1

    goto :goto_0

    :cond_3
    if-le p1, p3, :cond_4

    const/4 v0, 0x3

    goto :goto_0

    :cond_4
    const/4 v0, 0x2

    goto :goto_0

    :cond_5
    if-ge p1, p3, :cond_6

    const/4 v0, 0x0

    goto :goto_0

    :cond_6
    if-le p1, p3, :cond_7

    const/4 v0, 0x4

    goto :goto_0

    :cond_7
    const/16 v0, 0x8

    goto :goto_0
.end method

.method public static a(B)I
    .locals 1

    if-gez p0, :cond_0

    add-int/lit16 v0, p0, 0x100

    :goto_0
    return v0

    :cond_0
    move v0, p0

    goto :goto_0
.end method

.method public static a(I)I
    .locals 1

    sget-object v0, La/c/x;->j:Ljava/util/Random;

    invoke-virtual {v0}, Ljava/util/Random;->nextInt()I

    move-result v0

    shl-int/lit8 v0, v0, 0x1

    ushr-int/lit8 v0, v0, 0x1

    rem-int/2addr v0, p0

    return v0
.end method

.method public static a(II)I
    .locals 1

    sub-int v0, p1, p0

    invoke-static {v0}, La/c/x;->a(I)I

    move-result v0

    add-int/2addr v0, p0

    return v0
.end method

.method public static a(III)I
    .locals 1

    if-nez p1, :cond_0

    const/4 v0, 0x0

    :goto_0
    return v0

    :cond_0
    mul-int v0, p0, p2

    div-int/2addr v0, p1

    goto :goto_0
.end method

.method public static a(Ljavax/microedition/lcdui/Font;Ljava/lang/String;)I
    .locals 9

    const/4 v8, -0x1

    const/4 v2, 0x0

    invoke-virtual {p0, p1}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v3

    invoke-virtual {p0}, Ljavax/microedition/lcdui/Font;->e()I

    move-result v7

    invoke-static {v3, v7}, Ljavax/microedition/lcdui/Image;->a(II)Ljavax/microedition/lcdui/Image;

    move-result-object v0

    invoke-virtual {v0}, Ljavax/microedition/lcdui/Image;->a()Ljavax/microedition/lcdui/Graphics;

    move-result-object v1

    const v4, 0xffffff

    invoke-virtual {v1, v4}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    invoke-virtual {v1, v2, v2, v3, v7}, Ljavax/microedition/lcdui/Graphics;->c(IIII)V

    invoke-virtual {v1, v2}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    invoke-virtual {v1, p0}, Ljavax/microedition/lcdui/Graphics;->a(Ljavax/microedition/lcdui/Font;)V

    invoke-virtual {v1, p1, v2, v2, v2}, Ljavax/microedition/lcdui/Graphics;->a(Ljava/lang/String;III)V

    mul-int v1, v3, v7

    new-array v1, v1, [I

    iget-object v0, v0, Ljavax/microedition/lcdui/Image;->a:Landroid/graphics/Bitmap;

    move v4, v2

    move v5, v2

    move v6, v3

    invoke-virtual/range {v0 .. v7}, Landroid/graphics/Bitmap;->getPixels([IIIIIII)V

    array-length v0, v1

    const/4 v4, 0x1

    sub-int v4, v0, v4

    :goto_0
    if-ge v2, v0, :cond_0

    aget v5, v1, v2

    if-ne v5, v8, :cond_0

    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_0
    :goto_1
    if-lez v4, :cond_1

    if-ge v4, v0, :cond_1

    aget v5, v1, v4

    if-ne v5, v8, :cond_1

    add-int/lit8 v4, v4, -0x1

    goto :goto_1

    :cond_1
    sub-int/2addr v0, v4

    div-int/2addr v0, v3

    div-int v1, v2, v3

    sub-int/2addr v0, v1

    return v0
.end method

.method public static a(S)I
    .locals 1

    if-gez p0, :cond_0

    const/high16 v0, 0x10000

    add-int/2addr v0, p0

    :goto_0
    return v0

    :cond_0
    move v0, p0

    goto :goto_0
.end method

.method public static a([BI)I
    .locals 2

    aget-byte v0, p0, p1

    and-int/lit16 v0, v0, 0xff

    shl-int/lit8 v0, v0, 0x18

    add-int/lit8 v1, p1, 0x1

    aget-byte v1, p0, v1

    and-int/lit16 v1, v1, 0xff

    shl-int/lit8 v1, v1, 0x10

    or-int/2addr v0, v1

    add-int/lit8 v1, p1, 0x2

    aget-byte v1, p0, v1

    and-int/lit16 v1, v1, 0xff

    shl-int/lit8 v1, v1, 0x8

    or-int/2addr v0, v1

    add-int/lit8 v1, p1, 0x3

    aget-byte v1, p0, v1

    and-int/lit16 v1, v1, 0xff

    or-int/2addr v0, v1

    return v0
.end method

.method public static a(F)Ljava/lang/String;
    .locals 7

    const/4 v5, 0x2

    const/4 v4, 0x0

    const-string v6, "."

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    invoke-static {p0}, Ljava/lang/Float;->toString(F)Ljava/lang/String;

    move-result-object v1

    const-string v2, "."

    invoke-virtual {v1, v6}, Ljava/lang/String;->indexOf(Ljava/lang/String;)I

    move-result v2

    const/4 v3, -0x1

    if-ne v3, v2, :cond_0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "."

    invoke-virtual {v0, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "00"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :goto_0
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0

    :cond_0
    invoke-virtual {v1, v4, v2}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v0, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v3, "."

    invoke-virtual {v0, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    add-int/lit8 v2, v2, 0x1

    invoke-virtual {v1}, Ljava/lang/String;->length()I

    move-result v3

    invoke-virtual {v1, v2, v3}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/String;->length()I

    move-result v2

    if-le v2, v5, :cond_1

    invoke-virtual {v1, v4, v5}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_0

    :cond_1
    invoke-virtual {v1}, Ljava/lang/String;->length()I

    move-result v2

    if-ge v2, v5, :cond_2

    invoke-virtual {v1}, Ljava/lang/String;->length()I

    move-result v2

    invoke-virtual {v1, v4, v2}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v0, v4}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    goto :goto_0

    :cond_2
    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_0
.end method

.method public static a(La/c/p;Ljava/util/Vector;)Ljava/lang/StringBuffer;
    .locals 10

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    invoke-virtual {p0}, La/c/p;->d()Ljava/lang/StringBuffer;

    move-result-object p0

    const/4 v1, 0x0

    invoke-virtual {p0}, Ljava/lang/StringBuffer;->length()I

    move-result v2

    const/4 v3, 0x0

    const/4 v4, 0x0

    move v9, v4

    move v4, v1

    move v1, v9

    :goto_0
    if-ge v1, v2, :cond_c

    invoke-virtual {p0, v1}, Ljava/lang/StringBuffer;->charAt(I)C

    move-result v5

    const/16 v6, 0x5f

    if-ne v6, v5, :cond_1

    add-int/lit8 v4, v4, 0x1

    :cond_0
    :goto_1
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    :cond_1
    const/16 v6, 0x24

    if-ne v6, v5, :cond_0

    sub-int v5, v1, v3

    new-array v5, v5, [C

    const/4 v6, 0x0

    invoke-virtual {p0, v3, v1, v5, v6}, Ljava/lang/StringBuffer;->getChars(II[CI)V

    invoke-virtual {v0, v5}, Ljava/lang/StringBuffer;->append([C)Ljava/lang/StringBuffer;

    add-int/lit8 v3, v1, 0x1

    invoke-virtual {p0, v3}, Ljava/lang/StringBuffer;->charAt(I)C

    move-result v3

    const/16 v5, 0x6e

    if-ne v5, v3, :cond_2

    sget-object v3, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v3}, Lpmsj/work/b/ab;->p()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v0, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    add-int/lit8 v3, v1, 0x2

    goto :goto_1

    :cond_2
    const/16 v5, 0x73

    if-eq v5, v3, :cond_3

    const/16 v5, 0x6d

    if-ne v5, v3, :cond_a

    :cond_3
    move v5, v1

    :goto_2
    if-ge v5, v2, :cond_4

    invoke-virtual {p0, v5}, Ljava/lang/StringBuffer;->charAt(I)C

    move-result v6

    const/16 v7, 0x3e

    if-eq v6, v7, :cond_4

    add-int/lit8 v5, v5, 0x1

    goto :goto_2

    :cond_4
    if-eq v5, v2, :cond_f

    sub-int v6, v5, v1

    const/4 v7, 0x3

    sub-int/2addr v6, v7

    new-array v6, v6, [C

    add-int/lit8 v1, v1, 0x3

    const/4 v7, 0x0

    invoke-virtual {p0, v1, v5, v6, v7}, Ljava/lang/StringBuffer;->getChars(II[CI)V

    invoke-static {v6}, La/c/x;->a([C)Ljava/util/Vector;

    move-result-object v1

    const/16 v6, 0x73

    if-ne v6, v3, :cond_7

    sget-object v3, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    const/4 v6, 0x6

    invoke-virtual {v3, v6}, Lpmsj/work/b/ab;->f(B)I

    move-result v3

    invoke-static {v3}, Lpmsj/work/b/v;->x(I)B

    move-result v3

    if-nez v3, :cond_6

    const/4 v3, 0x0

    invoke-virtual {v1, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/Object;)Ljava/lang/StringBuffer;

    :cond_5
    :goto_3
    add-int/lit8 v1, v5, 0x1

    move v3, v1

    move v1, v5

    goto :goto_1

    :cond_6
    const/4 v3, 0x1

    invoke-virtual {v1, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/Object;)Ljava/lang/StringBuffer;

    goto :goto_3

    :cond_7
    if-eqz p1, :cond_5

    const/4 v3, 0x6

    new-array v3, v3, [La/c/i;

    const/4 v6, 0x0

    :goto_4
    const/4 v7, 0x3

    if-ge v6, v7, :cond_8

    new-instance v7, La/c/m;

    invoke-virtual {v1, v6}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v8

    invoke-virtual {v8}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v8

    invoke-static {v8}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v8

    invoke-direct {v7, v8}, La/c/m;-><init>(I)V

    aput-object v7, v3, v6

    add-int/lit8 v6, v6, 0x1

    goto :goto_4

    :cond_8
    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v6

    const/4 v7, 0x4

    if-ge v6, v7, :cond_9

    const/4 v6, 0x3

    new-instance v7, La/c/p;

    const-string v8, "\u5bfb\u8def"

    invoke-direct {v7, v8}, La/c/p;-><init>(Ljava/lang/String;)V

    aput-object v7, v3, v6

    :goto_5
    const/4 v6, 0x4

    new-instance v7, La/c/m;

    invoke-direct {v7, v4}, La/c/m;-><init>(I)V

    aput-object v7, v3, v6

    const/4 v6, 0x5

    new-instance v7, La/c/m;

    const/4 v8, 0x4

    invoke-virtual {v1, v8}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v1

    invoke-direct {v7, v1}, La/c/m;-><init>(I)V

    aput-object v7, v3, v6

    invoke-virtual {p1, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v1, "*4"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/4 v1, 0x3

    aget-object v1, v3, v1

    invoke-virtual {v1}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "*0"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_3

    :cond_9
    const/4 v6, 0x3

    new-instance v7, La/c/p;

    const/4 v8, 0x3

    invoke-virtual {v1, v8}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v8

    invoke-virtual {v8}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v8

    invoke-direct {v7, v8}, La/c/p;-><init>(Ljava/lang/String;)V

    aput-object v7, v3, v6

    goto :goto_5

    :cond_a
    add-int/lit8 v3, v1, 0x1

    invoke-virtual {p0, v3}, Ljava/lang/StringBuffer;->charAt(I)C

    move-result v3

    const/16 v5, 0x70

    if-ne v3, v5, :cond_b

    sget-object v3, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v3}, Lpmsj/work/b/ab;->U()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v0, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    add-int/lit8 v3, v1, 0x2

    goto/16 :goto_1

    :cond_b
    add-int/lit8 v3, v1, 0x1

    invoke-virtual {p0, v3}, Ljava/lang/StringBuffer;->charAt(I)C

    move-result v3

    const/16 v5, 0x72

    if-ne v3, v5, :cond_e

    sget-object v3, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v3}, Lpmsj/work/b/ab;->R()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v0, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    add-int/lit8 v3, v1, 0x2

    goto/16 :goto_1

    :cond_c
    if-ge v3, v2, :cond_d

    sub-int p1, v2, v3

    new-array p1, p1, [C

    const/4 v1, 0x0

    invoke-virtual {p0, v3, v2, p1, v1}, Ljava/lang/StringBuffer;->getChars(II[CI)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuffer;->append([C)Ljava/lang/StringBuffer;

    :cond_d
    return-object v0

    :cond_e
    move v3, v1

    goto/16 :goto_1

    :cond_f
    move v3, v5

    goto/16 :goto_1
.end method

.method public static a(Ljava/lang/StringBuffer;J)Ljava/lang/StringBuffer;
    .locals 1

    if-nez p0, :cond_0

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    :goto_0
    invoke-virtual {v0, p1, p2}, Ljava/lang/StringBuffer;->append(J)Ljava/lang/StringBuffer;

    return-object v0

    :cond_0
    move-object v0, p0

    goto :goto_0
.end method

.method public static a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;
    .locals 1

    if-nez p0, :cond_0

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    :goto_0
    invoke-virtual {v0, p1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    return-object v0

    :cond_0
    move-object v0, p0

    goto :goto_0
.end method

.method private static a([C)Ljava/util/Vector;
    .locals 6

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    new-instance v1, Ljava/lang/StringBuffer;

    invoke-direct {v1}, Ljava/lang/StringBuffer;-><init>()V

    const/4 v2, 0x0

    move v5, v2

    move-object v2, v1

    move v1, v5

    :goto_0
    array-length v3, p0

    if-ge v1, v3, :cond_1

    const/16 v3, 0x2c

    aget-char v4, p0, v1

    if-ne v3, v4, :cond_0

    invoke-virtual {v0, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    new-instance v2, Ljava/lang/StringBuffer;

    invoke-direct {v2}, Ljava/lang/StringBuffer;-><init>()V

    :goto_1
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    :cond_0
    aget-char v3, p0, v1

    invoke-virtual {v2, v3}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    goto :goto_1

    :cond_1
    invoke-virtual {v2}, Ljava/lang/StringBuffer;->length()I

    move-result v1

    if-lez v1, :cond_2

    invoke-virtual {v0, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_2
    return-object v0
.end method

.method public static a()V
    .locals 3

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x568ac0

    const/4 v2, 0x0

    invoke-direct {v0, v1, v2}, Lpmsj/work/a/i;-><init>(II)V

    sput-object v0, La/c/x;->g:Lpmsj/work/a/i;

    return-void
.end method

.method private static a(Ljava/util/Vector;Ljava/lang/String;Ljava/lang/String;)V
    .locals 3

    move-object v0, p1

    :goto_0
    invoke-virtual {v0, p2}, Ljava/lang/String;->indexOf(Ljava/lang/String;)I

    move-result v1

    const/4 v2, -0x1

    if-eq v1, v2, :cond_0

    const/4 v2, 0x0

    invoke-virtual {v0, v2, v1}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {p0, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v1, v1, 0x1

    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v2

    invoke-virtual {v0, v1, v2}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v0

    goto :goto_0

    :cond_0
    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v1

    if-eqz v1, :cond_1

    invoke-virtual {p0, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_1
    return-void
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;III)V
    .locals 6

    const/4 v5, 0x0

    rem-int/lit16 v0, p3, 0x3e8

    div-int/lit8 v0, v0, 0x64

    rem-int/lit8 v1, p3, 0x64

    div-int/lit8 v1, v1, 0xa

    rem-int/lit8 v2, p3, 0xa

    if-lez v0, :cond_0

    sget-object v3, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v3, v0}, Lpmsj/work/a/i;->a(I)V

    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    const/4 v3, 0x5

    sub-int v3, p1, v3

    sget-object v4, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v4}, Lpmsj/work/a/i;->b()I

    move-result v4

    sub-int v4, p2, v4

    invoke-virtual {v0, p0, v3, v4, v5}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v0, v1}, Lpmsj/work/a/i;->a(I)V

    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    sget-object v1, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v1}, Lpmsj/work/a/i;->b()I

    move-result v1

    sub-int v1, p2, v1

    invoke-virtual {v0, p0, p1, v1, v5}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v0, v2}, Lpmsj/work/a/i;->a(I)V

    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    add-int/lit8 v1, p1, 0x5

    sget-object v2, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v2}, Lpmsj/work/a/i;->b()I

    move-result v2

    sub-int v2, p2, v2

    invoke-virtual {v0, p0, v1, v2, v5}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    :goto_0
    return-void

    :cond_0
    if-lez v1, :cond_1

    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v0, v1}, Lpmsj/work/a/i;->a(I)V

    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    sget-object v1, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v1}, Lpmsj/work/a/i;->b()I

    move-result v1

    sub-int v1, p2, v1

    invoke-virtual {v0, p0, p1, v1, v5}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v0, v2}, Lpmsj/work/a/i;->a(I)V

    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    add-int/lit8 v1, p1, 0x5

    sget-object v2, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v2}, Lpmsj/work/a/i;->b()I

    move-result v2

    sub-int v2, p2, v2

    invoke-virtual {v0, p0, v1, v2, v5}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    goto :goto_0

    :cond_1
    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v0, v2}, Lpmsj/work/a/i;->a(I)V

    sget-object v0, La/c/x;->f:Lpmsj/work/a/i;

    sget-object v1, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v1}, Lpmsj/work/a/i;->b()I

    move-result v1

    sub-int v1, p2, v1

    invoke-virtual {v0, p0, p1, v1, v5}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    goto :goto_0
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;IIIB)V
    .locals 7

    const/4 v6, 0x2

    if-ge v6, p4, :cond_0

    move v4, v6

    :goto_0
    sget-object v0, La/c/x;->k:Lpmsj/work/a/i;

    const/4 v5, 0x0

    move-object v1, p0

    move v2, p1

    move v3, p2

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    sget-object v0, La/c/x;->l:Lpmsj/work/a/i;

    sget-object v1, La/c/x;->k:Lpmsj/work/a/i;

    invoke-virtual {v1}, Lpmsj/work/a/i;->c()I

    move-result v1

    add-int/2addr v1, p1

    sget-object v2, La/c/x;->k:Lpmsj/work/a/i;

    invoke-virtual {v2}, Lpmsj/work/a/i;->c()I

    move-result v2

    mul-int/lit8 v2, v2, 0x2

    sub-int v3, p3, v2

    move v2, p2

    move-object v5, p0

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/a/i;->a(IIIILjavax/microedition/lcdui/Graphics;)V

    sget-object v0, La/c/x;->k:Lpmsj/work/a/i;

    add-int v1, p1, p3

    sget-object v2, La/c/x;->k:Lpmsj/work/a/i;

    invoke-virtual {v2}, Lpmsj/work/a/i;->c()I

    move-result v2

    sub-int v2, v1, v2

    move-object v1, p0

    move v3, p2

    move v5, v6

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    return-void

    :cond_0
    move v4, p4

    goto :goto_0
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;IIIII)V
    .locals 0

    invoke-virtual {p0, p5}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    invoke-virtual {p0, p1, p2, p3, p4}, Ljavax/microedition/lcdui/Graphics;->b(IIII)V

    return-void
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;IIIIII)V
    .locals 9

    const/4 v8, 0x6

    const/4 v7, 0x5

    const/4 v6, 0x3

    invoke-virtual {p0, p6}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    invoke-virtual {p0, p1, p2, p3, p4}, Ljavax/microedition/lcdui/Graphics;->c(IIII)V

    and-int/lit8 v0, p5, 0x2

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    sub-int v3, p3, v0

    sget v5, Lpmsj/work/a/c;->M:I

    move-object v0, p0

    move v1, p1

    move v2, p2

    move v4, p4

    invoke-static/range {v0 .. v5}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIII)V

    add-int/lit8 v1, p1, 0x1

    add-int/lit8 v2, p2, 0x1

    sub-int v3, p3, v6

    const/4 v0, 0x2

    sub-int v4, p4, v0

    sget v5, Lpmsj/work/a/c;->N:I

    move-object v0, p0

    invoke-static/range {v0 .. v5}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIII)V

    add-int/lit8 v1, p1, 0x2

    add-int/lit8 v2, p2, 0x2

    sub-int v3, p3, v7

    const/4 v0, 0x4

    sub-int v4, p4, v0

    sget v5, Lpmsj/work/a/c;->O:I

    move-object v0, p0

    invoke-static/range {v0 .. v5}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIII)V

    add-int/lit8 v1, p1, 0x3

    add-int/lit8 v2, p2, 0x3

    const/4 v0, 0x7

    sub-int v3, p3, v0

    sub-int v4, p4, v8

    sget v5, Lpmsj/work/a/c;->M:I

    move-object v0, p0

    invoke-static/range {v0 .. v5}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIII)V

    add-int v0, p1, p3

    sget-object v1, La/c/x;->g:Lpmsj/work/a/i;

    invoke-virtual {v1}, Lpmsj/work/a/i;->c()I

    move-result v1

    sub-int/2addr v0, v1

    add-int v1, p2, p4

    sget-object v2, La/c/x;->g:Lpmsj/work/a/i;

    invoke-virtual {v2}, Lpmsj/work/a/i;->b()I

    move-result v2

    sub-int/2addr v1, v2

    add-int/lit8 v1, v1, 0x1

    sget-object v2, La/c/x;->g:Lpmsj/work/a/i;

    const/4 v3, 0x0

    invoke-virtual {v2, p0, p1, p2, v3}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    sget-object v2, La/c/x;->g:Lpmsj/work/a/i;

    invoke-virtual {v2, p0, v0, p2, v7}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    sget-object v2, La/c/x;->g:Lpmsj/work/a/i;

    invoke-virtual {v2, p0, p1, v1, v8}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    sget-object v2, La/c/x;->g:Lpmsj/work/a/i;

    invoke-virtual {v2, p0, v0, v1, v6}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    :cond_0
    return-void
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;IIIIIII)V
    .locals 6

    const/16 v3, 0x14

    const/4 v5, 0x0

    move-object v0, p0

    move v1, p1

    move v2, p2

    move v4, p3

    invoke-static/range {v0 .. v5}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIII)V

    add-int/lit8 v1, p1, 0x1

    add-int/lit8 v2, p2, 0x1

    const/16 v3, 0x13

    const/4 v0, 0x1

    sub-int v4, p3, v0

    const v5, 0x3e3e3e

    move-object v0, p0

    invoke-static/range {v0 .. v5}, La/c/x;->b(Ljavax/microedition/lcdui/Graphics;IIIII)V

    invoke-static {p7}, Ljava/lang/Math;->abs(I)I

    move-result v0

    add-int/2addr v0, p4

    const/16 v1, 0x14

    invoke-static {p7}, Ljava/lang/Math;->abs(I)I

    move-result v2

    invoke-static {v1, v0, v2}, La/c/x;->a(III)I

    move-result v3

    if-lez p7, :cond_1

    sget-byte v0, Lpmsj/work/a/c;->q:B

    invoke-static {v0}, Lpmsj/work/a/c;->a(B)I

    move-result v0

    invoke-virtual {p0, v0}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    add-int/lit8 v0, p1, 0x14

    add-int v1, p2, p3

    sub-int v2, v0, v3

    invoke-virtual {p0, v0, p2, v2, p2}, Ljavax/microedition/lcdui/Graphics;->a(IIII)V

    invoke-virtual {p0, v0, p2, v0, v1}, Ljavax/microedition/lcdui/Graphics;->a(IIII)V

    sub-int v2, v0, v3

    invoke-virtual {p0, v0, v1, v2, v1}, Ljavax/microedition/lcdui/Graphics;->a(IIII)V

    :cond_0
    :goto_0
    if-gez p7, :cond_2

    const/16 v0, 0x13

    sub-int/2addr v0, v3

    :goto_1
    add-int/2addr p4, p7

    invoke-static {v0, p4, p5}, La/c/x;->a(III)I

    move-result p4

    if-nez p4, :cond_3

    if-lez p5, :cond_3

    const/4 p4, 0x1

    move v3, p4

    :goto_2
    add-int/lit8 v1, p1, 0x1

    add-int/lit8 v2, p2, 0x1

    const/4 p1, 0x1

    sub-int v4, p3, p1

    move-object v0, p0

    move v5, p6

    invoke-static/range {v0 .. v5}, La/c/x;->b(Ljavax/microedition/lcdui/Graphics;IIIII)V

    return-void

    :cond_1
    if-gez p7, :cond_0

    add-int/lit8 v0, p1, 0x14

    sub-int v1, v0, v3

    const v5, 0xa8a8a8

    move-object v0, p0

    move v2, p2

    move v4, p3

    invoke-static/range {v0 .. v5}, La/c/x;->b(Ljavax/microedition/lcdui/Graphics;IIIII)V

    goto :goto_0

    :cond_2
    const/16 v0, 0x13

    goto :goto_1

    :cond_3
    move v3, p4

    goto :goto_2
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;IIIIIIII)V
    .locals 4

    const/4 v3, 0x1

    invoke-virtual {p0, p8}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    add-int/lit8 v0, p1, 0x1

    add-int/lit8 v1, p2, 0x1

    sub-int v2, p4, v3

    invoke-virtual {p0, v0, v1, p3, v2}, Ljavax/microedition/lcdui/Graphics;->c(IIII)V

    if-nez p6, :cond_1

    move v0, v3

    :goto_0
    invoke-virtual {p0, p7}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    mul-int v1, p3, p5

    div-int v0, v1, v0

    if-nez v0, :cond_0

    if-lez p5, :cond_0

    move v0, v3

    :cond_0
    add-int/lit8 v1, p1, 0x1

    add-int/lit8 v2, p2, 0x1

    sub-int v3, p4, v3

    invoke-virtual {p0, v1, v2, v0, v3}, Ljavax/microedition/lcdui/Graphics;->c(IIII)V

    const/4 v0, 0x0

    invoke-virtual {p0, v0}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    add-int/lit8 v0, p3, 0x1

    invoke-virtual {p0, p1, p2, v0, p4}, Ljavax/microedition/lcdui/Graphics;->b(IIII)V

    return-void

    :cond_1
    move v0, p6

    goto :goto_0
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;II)V
    .locals 1

    sget v0, Lpmsj/work/a/c;->y:I

    invoke-virtual {p0, v0}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    const/4 v0, 0x0

    invoke-virtual {p0, p1, p2, p3, v0}, Ljavax/microedition/lcdui/Graphics;->a(Ljava/lang/String;III)V

    return-void
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;III)V
    .locals 1

    invoke-virtual {p0, p4}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    const/4 v0, 0x0

    invoke-virtual {p0, p1, p2, p3, v0}, Ljavax/microedition/lcdui/Graphics;->a(Ljava/lang/String;III)V

    return-void
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;IILjavax/microedition/lcdui/Font;II)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, p4}, Ljavax/microedition/lcdui/Graphics;->a(Ljavax/microedition/lcdui/Font;)V

    invoke-virtual {p0, p6}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    add-int/lit8 v0, p2, 0x1

    add-int/lit8 v1, p3, 0x1

    invoke-virtual {p0, p1, v0, v1, v2}, Ljavax/microedition/lcdui/Graphics;->a(Ljava/lang/String;III)V

    invoke-virtual {p0, p5}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    invoke-virtual {p0, p1, p2, p3, v2}, Ljavax/microedition/lcdui/Graphics;->a(Ljava/lang/String;III)V

    return-void
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/a/i;Lpmsj/work/a/i;III)V
    .locals 7

    const/4 v6, 0x0

    move-object v0, p0

    move-object v1, p1

    move-object v2, p2

    move v3, p3

    move v4, p4

    move v5, p5

    invoke-static/range {v0 .. v6}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/a/i;Lpmsj/work/a/i;IIII)V

    return-void
.end method

.method public static a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/a/i;Lpmsj/work/a/i;IIII)V
    .locals 3

    const/4 v2, 0x2

    if-lez p5, :cond_0

    const/4 v0, 0x0

    invoke-virtual {p1, p0, p3, p4, v0}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    :cond_0
    if-nez p6, :cond_2

    invoke-virtual {p1}, Lpmsj/work/a/i;->c()I

    move-result v0

    add-int/2addr v0, p3

    invoke-virtual {p1}, Lpmsj/work/a/i;->c()I

    move-result v1

    mul-int/lit8 v1, v1, 0x2

    sub-int v1, p5, v1

    invoke-virtual {p2, v0, p4, v1, p0}, Lpmsj/work/a/i;->a(IIILjavax/microedition/lcdui/Graphics;)V

    add-int v0, p3, p5

    invoke-virtual {p1}, Lpmsj/work/a/i;->c()I

    move-result v1

    sub-int/2addr v0, v1

    invoke-virtual {p1, p0, v0, p4, v2}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    :cond_1
    :goto_0
    return-void

    :cond_2
    invoke-virtual {p1}, Lpmsj/work/a/i;->c()I

    move-result v0

    if-le p5, v0, :cond_3

    invoke-virtual {p1}, Lpmsj/work/a/i;->c()I

    move-result v0

    add-int/2addr v0, p3

    invoke-virtual {p1}, Lpmsj/work/a/i;->c()I

    move-result v1

    sub-int v1, p5, v1

    invoke-virtual {p2, v0, p4, v1, p0}, Lpmsj/work/a/i;->a(IIILjavax/microedition/lcdui/Graphics;)V

    :cond_3
    invoke-virtual {p1}, Lpmsj/work/a/i;->c()I

    move-result v0

    sub-int v0, p6, v0

    if-le p5, v0, :cond_1

    add-int v0, p3, p6

    invoke-virtual {p1}, Lpmsj/work/a/i;->c()I

    move-result v1

    sub-int/2addr v0, v1

    invoke-virtual {p1, p0, v0, p4, v2}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    goto :goto_0
.end method

.method public static a([BII)V
    .locals 2

    const/high16 v0, -0x1000000

    and-int/2addr v0, p2

    shr-int/lit8 v0, v0, 0x18

    int-to-byte v0, v0

    aput-byte v0, p0, p1

    add-int/lit8 v0, p1, 0x1

    const/high16 v1, 0xff0000

    and-int/2addr v1, p2

    shr-int/lit8 v1, v1, 0x10

    int-to-byte v1, v1

    aput-byte v1, p0, v0

    add-int/lit8 v0, p1, 0x2

    const v1, 0xff00

    and-int/2addr v1, p2

    shr-int/lit8 v1, v1, 0x8

    int-to-byte v1, v1

    aput-byte v1, p0, v0

    add-int/lit8 v0, p1, 0x3

    and-int/lit16 v1, p2, 0xff

    int-to-byte v1, v1

    aput-byte v1, p0, v0

    return-void
.end method

.method public static a([BIS)V
    .locals 2

    const v0, 0xff00

    and-int/2addr v0, p2

    shr-int/lit8 v0, v0, 0x8

    int-to-byte v0, v0

    aput-byte v0, p0, p1

    add-int/lit8 v0, p1, 0x1

    and-int/lit16 v1, p2, 0xff

    int-to-byte v1, v1

    aput-byte v1, p0, v0

    return-void
.end method

.method public static a(IIIIII)Z
    .locals 1

    if-lt p0, p2, :cond_0

    if-gt p0, p3, :cond_0

    if-lt p1, p4, :cond_0

    if-gt p1, p5, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static a(Ljava/lang/String;)Z
    .locals 5

    const/4 v4, 0x0

    :try_start_0
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v0

    move v1, v4

    :goto_0
    if-ge v1, v0, :cond_4

    invoke-virtual {p0, v1}, Ljava/lang/String;->charAt(I)C
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result v2

    const/16 v3, 0x20

    if-eq v2, v3, :cond_3

    const/16 v3, 0x30

    if-lt v2, v3, :cond_0

    const/16 v3, 0x39

    if-le v2, v3, :cond_3

    :cond_0
    const/16 v3, 0x41

    if-lt v2, v3, :cond_1

    const/16 v3, 0x5a

    if-le v2, v3, :cond_3

    :cond_1
    const/16 v3, 0x61

    if-lt v2, v3, :cond_2

    const/16 v3, 0x7a

    if-le v2, v3, :cond_3

    :cond_2
    move v0, v4

    :goto_1
    return v0

    :cond_3
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    :catch_0
    move-exception v0

    move v0, v4

    goto :goto_1

    :cond_4
    const/4 v0, 0x1

    goto :goto_1
.end method

.method private static a(Ljava/io/InputStream;)[B
    .locals 6

    const/4 v5, 0x0

    const/4 v4, 0x2

    const/4 v3, 0x0

    if-nez p0, :cond_0

    move-object v0, v5

    :goto_0
    return-object v0

    :cond_0
    const/4 v0, 0x2

    :try_start_0
    new-array v0, v0, [B
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    :try_start_1
    invoke-virtual {p0, v0}, Ljava/io/InputStream;->read([B)I
    :try_end_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0

    :goto_1
    if-eqz p0, :cond_3

    :try_start_2
    array-length v1, v0

    const/4 v2, 0x1

    if-ne v1, v2, :cond_1

    const/4 v1, 0x0

    aget-byte v0, v0, v1

    :goto_2
    new-array v1, v0, [B

    const/4 v2, 0x0

    invoke-virtual {p0, v1, v2, v0}, Ljava/io/InputStream;->read([BII)I

    invoke-virtual {p0}, Ljava/io/InputStream;->close()V

    move-object v0, v1

    goto :goto_0

    :cond_1
    array-length v1, v0

    if-ne v1, v4, :cond_2

    const/4 v1, 0x0

    invoke-static {v0, v1}, La/c/x;->b([BI)S

    move-result v0

    goto :goto_2

    :cond_2
    array-length v1, v0

    const/4 v2, 0x4

    if-ne v1, v2, :cond_5

    const/4 v1, 0x0

    invoke-static {v0, v1}, La/c/x;->a([BI)I

    move-result v0

    goto :goto_2

    :cond_3
    array-length v1, v0

    new-array v2, v1, [B

    :goto_3
    if-ge v3, v1, :cond_4

    aget-byte v4, v0, v3

    aput-byte v4, v2, v3
    :try_end_2
    .catch Ljava/lang/Exception; {:try_start_2 .. :try_end_2} :catch_0

    add-int/lit8 v3, v3, 0x1

    goto :goto_3

    :catch_0
    move-exception v0

    move-object v0, v5

    goto :goto_0

    :catch_1
    move-exception v1

    goto :goto_1

    :cond_4
    move-object v0, v2

    goto :goto_0

    :cond_5
    move v0, v3

    goto :goto_2
.end method

.method public static a(Ljava/io/InputStream;I)[B
    .locals 2

    :try_start_0
    new-array v0, p1, [B

    const/4 v1, 0x0

    invoke-virtual {p0, v0, v1, p1}, Ljava/io/InputStream;->read([BII)I
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    :goto_0
    return-object v0

    :catch_0
    move-exception v0

    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static a(IILpmsj/work/main/w;)[La/c/i;
    .locals 4

    new-array v1, p0, [La/c/i;

    const/4 v0, 0x0

    move v2, v0

    :goto_0
    if-ge v2, p0, :cond_0

    iget-object v0, p2, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int v3, v2, p1

    invoke-virtual {v0, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    aput-object v0, v1, v2

    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_0

    :cond_0
    return-object v1
.end method

.method public static a(Ljava/lang/String;Ljava/lang/String;)[Ljava/lang/String;
    .locals 4

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    invoke-static {v0, p0, p1}, La/c/x;->a(Ljava/util/Vector;Ljava/lang/String;Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v1

    new-array v2, v1, [Ljava/lang/String;

    const/4 v3, 0x0

    :goto_0
    if-ge v3, v1, :cond_0

    invoke-virtual {v0, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Ljava/lang/String;

    aput-object p0, v2, v3

    add-int/lit8 v3, v3, 0x1

    goto :goto_0

    :cond_0
    return-object v2
.end method

.method public static b(I)Ljava/lang/String;
    .locals 2

    if-gtz p0, :cond_0

    const-string v0, ""

    :goto_0
    return-object v0

    :cond_0
    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    div-int/lit16 v1, p0, 0xe10

    if-lez v1, :cond_1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    const-string v1, "\u65f6"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :cond_1
    rem-int/lit16 v1, p0, 0xe10

    div-int/lit8 v1, v1, 0x3c

    if-lez v1, :cond_2

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    const-string v1, "\u5206"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :cond_2
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    goto :goto_0
.end method

.method public static b(B)S
    .locals 1

    if-gez p0, :cond_0

    add-int/lit16 v0, p0, 0x100

    int-to-short v0, v0

    :goto_0
    return v0

    :cond_0
    int-to-short v0, p0

    goto :goto_0
.end method

.method public static b([BI)S
    .locals 2

    aget-byte v0, p0, p1

    and-int/lit16 v0, v0, 0xff

    shl-int/lit8 v0, v0, 0x8

    add-int/lit8 v1, p1, 0x1

    aget-byte v1, p0, v1

    and-int/lit16 v1, v1, 0xff

    or-int/2addr v0, v1

    int-to-short v0, v0

    return v0
.end method

.method public static b(Ljavax/microedition/lcdui/Graphics;IIIII)V
    .locals 0

    invoke-virtual {p0, p5}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    invoke-virtual {p0, p1, p2, p3, p4}, Ljavax/microedition/lcdui/Graphics;->c(IIII)V

    return-void
.end method

.method public static b(Ljavax/microedition/lcdui/Graphics;IIIIIII)V
    .locals 7

    add-int/lit8 v1, p1, 0x1

    add-int/lit8 v2, p2, 0x1

    const/4 v0, 0x2

    sub-int v3, p3, v0

    const/4 v0, 0x2

    sub-int v4, p4, v0

    const/4 v5, 0x0

    move-object v0, p0

    move v6, p5

    invoke-static/range {v0 .. v6}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIIII)V

    invoke-virtual {p0, p6}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    add-int p5, p1, p3

    const/4 p6, 0x2

    sub-int/2addr p5, p6

    invoke-virtual {p0, p1, p2, p5, p2}, Ljavax/microedition/lcdui/Graphics;->a(IIII)V

    add-int/lit8 p5, p2, 0x1

    add-int p6, p2, p4

    const/4 v0, 0x2

    sub-int/2addr p6, v0

    invoke-virtual {p0, p1, p5, p1, p6}, Ljavax/microedition/lcdui/Graphics;->a(IIII)V

    invoke-virtual {p0, p7}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    add-int p5, p1, p3

    const/4 p6, 0x1

    sub-int/2addr p5, p6

    add-int/lit8 p6, p2, 0x1

    add-int p7, p1, p3

    const/4 v0, 0x1

    sub-int/2addr p7, v0

    add-int v0, p2, p4

    const/4 v1, 0x1

    sub-int/2addr v0, v1

    invoke-virtual {p0, p5, p6, p7, v0}, Ljavax/microedition/lcdui/Graphics;->a(IIII)V

    add-int/lit8 p5, p1, 0x1

    add-int p6, p2, p4

    const/4 p7, 0x1

    sub-int/2addr p6, p7

    add-int/2addr p1, p3

    const/4 p3, 0x1

    sub-int/2addr p1, p3

    add-int/2addr p2, p4

    const/4 p3, 0x1

    sub-int/2addr p2, p3

    invoke-virtual {p0, p5, p6, p1, p2}, Ljavax/microedition/lcdui/Graphics;->a(IIII)V

    return-void
.end method

.method public static b(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;III)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    add-int/lit8 v0, p2, 0x1

    add-int/lit8 v1, p3, 0x1

    invoke-virtual {p0, p1, v0, v1, v2}, Ljavax/microedition/lcdui/Graphics;->a(Ljava/lang/String;III)V

    invoke-virtual {p0, p4}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    invoke-virtual {p0, p1, p2, p3, v2}, Ljavax/microedition/lcdui/Graphics;->a(Ljava/lang/String;III)V

    return-void
.end method

.method public static b(Ljava/lang/String;)Z
    .locals 4

    const/4 v3, 0x0

    :try_start_0
    const-string v0, "@"

    invoke-virtual {p0, v0}, Ljava/lang/String;->indexOf(Ljava/lang/String;)I

    move-result v0

    const/4 v1, -0x1

    if-eq v0, v1, :cond_0

    const/4 v1, 0x0

    invoke-virtual {p0, v1, v0}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, La/c/x;->a(Ljava/lang/String;)Z

    move-result v1

    if-nez v1, :cond_1

    :cond_0
    move v0, v3

    :goto_0
    return v0

    :cond_1
    const-string v1, ".com"

    invoke-virtual {p0, v1}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_2

    add-int/lit8 v0, v0, 0x1

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v1

    const/4 v2, 0x4

    sub-int/2addr v1, v2

    invoke-virtual {p0, v0, v1}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v0

    :goto_1
    invoke-static {v0}, La/c/x;->a(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_4

    move v0, v3

    goto :goto_0

    :cond_2
    const-string v1, ".cn"

    invoke-virtual {p0, v1}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_3

    add-int/lit8 v0, v0, 0x1

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v1

    const/4 v2, 0x3

    sub-int/2addr v1, v2

    invoke-virtual {p0, v0, v1}, Ljava/lang/String;->substring(II)Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v0

    goto :goto_1

    :cond_3
    move v0, v3

    goto :goto_0

    :catch_0
    move-exception v0

    move v0, v3

    goto :goto_0

    :cond_4
    const/4 v0, 0x1

    goto :goto_0
.end method

.method public static c(I)Ljava/lang/String;
    .locals 9

    const/4 v8, 0x0

    const/16 v6, 0x9

    const-string v7, "0"

    const-string v5, ":"

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    div-int/lit16 v0, p0, 0xe10

    rem-int/lit16 v1, p0, 0xe10

    div-int/lit8 v1, v1, 0x3c

    rem-int/lit16 v2, p0, 0xe10

    rem-int/lit8 v2, v2, 0x3c

    if-le v0, v6, :cond_0

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v3, ":"

    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v8, v0}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    move-result-object v0

    :goto_0
    if-le v1, v6, :cond_1

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v3, ":"

    invoke-virtual {v1, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    move-result-object v0

    :goto_1
    if-le v2, v6, :cond_2

    int-to-long v1, v2

    invoke-static {v0, v1, v2}, La/c/x;->a(Ljava/lang/StringBuffer;J)Ljava/lang/StringBuffer;

    move-result-object v0

    :goto_2
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0

    :cond_0
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "0"

    invoke-virtual {v3, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v3, ":"

    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v8, v0}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    move-result-object v0

    goto :goto_0

    :cond_1
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "0"

    invoke-virtual {v3, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v3, ":"

    invoke-virtual {v1, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    move-result-object v0

    goto :goto_1

    :cond_2
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "0"

    invoke-virtual {v1, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    move-result-object v0

    goto :goto_2
.end method

.method public static c(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;III)V
    .locals 8

    const/4 v5, 0x0

    if-eqz p1, :cond_0

    const-string v0, ""

    if-eq p1, v0, :cond_0

    invoke-virtual {p1}, Ljava/lang/String;->length()I

    move-result v6

    move v7, v5

    move v2, p3

    :goto_0
    if-ge v7, v6, :cond_0

    invoke-virtual {p1, v7}, Ljava/lang/String;->charAt(I)C

    move-result v0

    const/4 v1, 0x1

    invoke-static {v0, v1}, Lpmsj/work/d/e;->a(CI)I

    move-result v4

    sget-object v0, La/c/x;->m:Lpmsj/work/a/i;

    move-object v1, p0

    move v3, p4

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    sget-object v0, La/c/x;->m:Lpmsj/work/a/i;

    invoke-virtual {v0}, Lpmsj/work/a/i;->c()I

    move-result v0

    add-int/2addr v0, p2

    add-int/2addr v0, v2

    add-int/lit8 v1, v7, 0x1

    move v7, v1

    move v2, v0

    goto :goto_0

    :cond_0
    return-void
.end method

.method public static c(Ljava/lang/String;)[B
    .locals 3

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    sget-object v1, Lpmsj/work/a/c;->Y:[Ljava/lang/String;

    const/4 v2, 0x0

    aget-object v1, v1, v2

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v0, p0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :try_start_0
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lpmsj/work/a/d;->a(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object v0

    invoke-static {v0}, La/c/x;->a(Ljava/io/InputStream;)[B
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v0

    :goto_0
    return-object v0

    :catch_0
    move-exception v0

    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static d(I)I
    .locals 2

    rem-int/lit16 v0, p0, 0x2710

    div-int/lit8 v0, v0, 0x64

    const v1, 0x2dc6c0

    mul-int/lit16 v0, v0, 0x2710

    add-int/2addr v0, v1

    add-int/lit16 v0, v0, 0x978

    mul-int/lit8 v0, v0, 0x64

    rem-int/lit8 v1, p0, 0x64

    add-int/2addr v0, v1

    return v0
.end method

.method public static d(Ljava/lang/String;)Z
    .locals 4

    const/16 v1, 0x13

    const/4 v3, 0x1

    const/4 v2, 0x0

    :try_start_0
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v0

    if-nez v0, :cond_0

    move v0, v3

    :goto_0
    return v0

    :cond_0
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v0

    if-le v0, v1, :cond_1

    const/4 v0, 0x0

    const/16 v1, 0x12

    invoke-virtual {p0, v0, v1}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/Long;->parseLong(Ljava/lang/String;)J

    const/16 v0, 0x13

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v1

    invoke-virtual {p0, v0, v1}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/Long;->parseLong(Ljava/lang/String;)J

    :goto_1
    move v0, v3

    goto :goto_0

    :cond_1
    invoke-static {p0}, Ljava/lang/Long;->parseLong(Ljava/lang/String;)J
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_1

    :catch_0
    move-exception v0

    move v0, v2

    goto :goto_0
.end method

.method public static e(Ljava/lang/String;)Ljava/lang/String;
    .locals 3

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v0

    const/4 v1, 0x5

    if-le v0, v1, :cond_0

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const/4 v1, 0x0

    const/4 v2, 0x4

    invoke-virtual {p0, v1, v2}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "..."

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    :goto_0
    return-object v0

    :cond_0
    move-object v0, p0

    goto :goto_0
.end method

.method public static e(I)Lpmsj/work/a/i;
    .locals 3

    rem-int/lit8 v0, p0, 0x64

    rem-int/lit16 v1, p0, 0x2710

    div-int/lit8 v1, v1, 0x64

    const v2, 0x2dc6c0

    mul-int/lit16 v1, v1, 0x2710

    add-int/2addr v1, v2

    add-int/lit16 v1, v1, 0x978

    new-instance v2, Lpmsj/work/a/i;

    invoke-direct {v2, v1, v0}, Lpmsj/work/a/i;-><init>(II)V

    return-object v2
.end method

.method public static f(I)Lpmsj/work/a/i;
    .locals 3

    rem-int/lit8 v0, p0, 0x64

    rem-int/lit16 v1, p0, 0x2710

    div-int/lit8 v1, v1, 0x64

    const v2, 0x2dc6c0

    mul-int/lit16 v1, v1, 0x2710

    add-int/2addr v1, v2

    add-int/lit16 v1, v1, 0x978

    new-instance v2, Lpmsj/work/a/i;

    invoke-direct {v2, v1, v0}, Lpmsj/work/a/i;-><init>(II)V

    return-object v2
.end method

.method public static g(I)Ljava/lang/String;
    .locals 1

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    invoke-virtual {v0, p0}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method
